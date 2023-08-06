import abc
import sys
import re
import numpy as np
import warnings

from ..common.python_utils import versiontuple2tuple

# Ensure compatibility with Python 2/3
ABC = abc.ABC if sys.version_info >= (3, 4) else abc.ABCMeta(str('ABC'), (), {})


class Interpreter(ABC):
    """
    Interpreter is the base abstract class for all Interpreters. 
    The implementation of any Interpreter should at least 

        **(1)** prepare :py:attr:`predict_fn` that outputs probability predictions, gradients or other desired 
        intermediate results of the model, and 

        **(2)** implement the core function :py:meth:`interpret` of the interpretation algorithm.
    In general, we find this implementation is practical, makes the code more readable and can highlight the core 
    function of the interpretation algorithm.

    This kind of implementation works for all post-poc interpretation algorithms. While some algorithms may have 
    different features and other fashions of implementations may be more suitable for them, our style of implementation
    can still work for most of them. So we follow this design for all Interpreters in this library.
    
    Three sub-abstract Interpreters that implement :py:meth:`_build_predict_fn` are currently provided in this file:
    :class:`InputGradientInterpreter`, :class:`InputOutputInterpreter`, :class:`IntermediateLayerInterpreter`. For each
    of them, the implemented :py:attr:`predict_fn` can be used by several different algorithms. Therefore, the further 
    implementations can focus on the core algorithm. More sub-abstract Interpreters will be provided if necessary.

    .. warning:: ``use_cuda`` would be deprecated soon. Use ``device`` directly.
    """

    def __init__(self, model: callable, device: str, **kwargs):
        """
        
        Args:
            model (callable): A model with :py:func:`forward` and possibly :py:func:`backward` functions.
            device (str): The device used for running ``model``, options: ``"cpu"``, ``"gpu:0"``, ``"gpu:1"`` 
                etc.
        """
        self.device = device
        self.model = model
        self.predict_fn = None

        if 'use_cuda' in kwargs and kwargs['use_cuda'] in [True, False]:
            warnings.warn('``use_cuda`` would be deprecated soon. Use ``device`` directly.', stacklevel=2)
            self.device = 'gpu:0' if kwargs['use_cuda'] and device[:3] == 'gpu' else 'cpu'

        assert self.device[:3] in ['cpu', 'gpu']

    def interpret(self, **kwargs):
        """Main function of the interpreter."""
        raise NotImplementedError

    def _build_predict_fn(self, **kwargs):
        """ Build :py:attr:`predict_fn` for interpreters. This will be called by :py:meth:`interpret`. """
        raise NotImplementedError

    def _env_setup(self):
        """Prepare the environment setup. This is not always necessary because the setup can be done within the 
        function of :py:func:`_build_predict_fn`.
        """
        #######################################################################
        # This is a simple implementation for disabling gradient computation. #
        #######################################################################
        import paddle
        assert versiontuple2tuple(paddle.__version__) >= (2, 2, 1)
        if not paddle.is_compiled_with_cuda() and self.device[:3] == 'gpu':
            print("Paddle is not installed with GPU support. Change to CPU version now.")
            self.device = 'cpu'

        # globally set device.
        paddle.set_device(self.device)

        # does not need gradients at all.
        self.model.eval()


class InputGradientInterpreter(Interpreter):
    """This is one of the sub-abstract Interpreters. 
    
    :class:`InputGradientInterpreter` are used by input gradient based Interpreters. Interpreters that are derived from 
    :class:`InputGradientInterpreter` include :class:`GradShapCVInterpreter`, :class:`IntGradCVInterpreter`, 
    :class:`SmoothGradInterpreter`.

    This Interpreter implements :py:func:`_build_predict_fn` that returns input gradient given an input. 
    """

    def __init__(self, model: callable, device: str, **kwargs):
        """
        
        Args:
            model (callable): A model with :py:func:`forward` and possibly :py:func:`backward` functions.
            device (str): The device used for running ``model``, options: ``"cpu"``, ``"gpu:0"``, ``"gpu:1"`` 
                etc.
        """
        Interpreter.__init__(self, model, device, **kwargs)
        assert hasattr(model, 'forward'), \
            "model has to be " \
            "an instance of paddle.nn.Layer or a compatible one."

    def _build_predict_fn(self, rebuild: bool = False, gradient_of: str = 'probability'):
        """Build ``predict_fn`` for input gradients based algorithms.
        The model is supposed to be a classification model.

        Args:
            rebuild (bool, optional): forces to rebuild. Defaults to ``False``.
            gradient_of (str, optional): computes the gradient of 
                [``"loss"``, ``"logit"`` or ``"probability"``] *w.r.t.* input data. Defaults to ``"probability"``. 
                Other options can get similar results while the absolute scale might be different.
        """

        if self.predict_fn is not None:
            assert callable(self.predict_fn), "predict_fn is predefined before, but is not callable." \
                "Check it again."

        if self.predict_fn is None or rebuild:
            assert gradient_of in ['loss', 'logit', 'probability']

            self._env_setup()

            def predict_fn(inputs, labels=None):
                """predict_fn for input gradients based interpreters,
                    for image classification models only.

                Args:
                    inputs ([type]): scaled inputs.
                    labels ([type]): can be None.

                Returns:
                    [type]: gradients, labels
                """
                import paddle
                # assert len(data.shape) == 4  # [bs, h, w, 3]
                assert labels is None or \
                    (isinstance(labels, (list, np.ndarray)) and len(labels) == inputs.shape[0])

                if isinstance(inputs, tuple):
                    tensor_inputs = []
                    for inp in inputs:
                        tmp = paddle.to_tensor(inp)
                        tmp.stop_gradient = False
                        tensor_inputs.append(tmp)
                    tensor_inputs = tuple(tensor_inputs)
                else:
                    tensor_inputs = paddle.to_tensor(inputs)
                    tensor_inputs.stop_gradient = False
                    tensor_inputs = (tensor_inputs, )

                # get logits and probas, [bs, num_c]
                logits = self.model(*tensor_inputs)
                num_samples, num_classes = logits.shape[0], logits.shape[1]
                probas = paddle.nn.functional.softmax(logits, axis=-1)

                # get predictions.
                pred = paddle.argmax(logits, axis=1)
                if labels is None:
                    labels = pred.numpy()

                # get gradients
                if gradient_of == 'loss':
                    # cross-entropy loss
                    loss = paddle.nn.functional.cross_entropy(logits, paddle.to_tensor(labels), reduction='sum')
                else:
                    # logits or probas
                    labels = np.array(labels).reshape((num_samples, ))
                    labels_onehot = paddle.nn.functional.one_hot(paddle.to_tensor(labels), num_classes=num_classes)
                    if gradient_of == 'logit':
                        loss = paddle.sum(logits * labels_onehot, axis=1)
                    else:
                        loss = paddle.sum(probas * labels_onehot, axis=1)

                loss.backward()
                gradients = tensor_inputs[0].grad
                if isinstance(gradients, paddle.Tensor):
                    gradients = gradients.numpy()

                return gradients, labels, probas

            self.predict_fn = predict_fn


class InputOutputInterpreter(Interpreter):
    """This is one of the sub-abstract Interpreters. 
    
    :class:`InputOutputInterpreter` are used by input-output correlation based Interpreters. Interpreters that are derived
    from :class:`InputOutputInterpreter` include :class:`OcclusionInterpreter`, :class:`LIMECVInterpreter`, 
    :class:`SmoothGradInterpreter`.

    This Interpreter implements :py:func:`_build_predict_fn` that returns the model's prediction given an input. 

    """

    def __init__(self, model: callable, device: str, **kwargs):
        """
        
        Args:
            model (callable): A model with :py:func:`forward` and possibly :py:func:`backward` functions.
            device (str): The device used for running ``model``, options: ``"cpu"``, ``"gpu:0"``, ``"gpu:1"`` 
                etc.
        """
        Interpreter.__init__(self, model, device, **kwargs)
        assert hasattr(model, 'forward'), \
            "model has to be " \
            "an instance of paddle.nn.Layer or a compatible one."

    def _build_predict_fn(self, rebuild: bool = False, output: str = 'probability'):
        """Build :py:attr:`predict_fn` for Input-Output based algorithms.
        The model is supposed to be a classification model.

        Args:
            rebuild (bool, optional): forces to rebuild. Defaults to ``False``.
            output (str, optional): computes the logit or probability. Defaults: ``"probability"``. Other options can 
                get similar results while the absolute scale might be different.
        """

        if self.predict_fn is not None:
            assert callable(self.predict_fn), "predict_fn is predefined before, but is not callable." \
                "Check it again."

        if self.predict_fn is None or rebuild:
            assert output in ['logit', 'probability']

            self._env_setup()

            def predict_fn(inputs, label):
                """predict_fn for input gradients based interpreters,
                    for image classification models only.

                Args:
                    inputs ([type]): [description]
                    label ([type]): can be None.

                Returns:
                    [type]: [description]
                """
                import paddle
                # assert len(inputs.shape) == 4  # [bs, h, w, 3]

                with paddle.no_grad():
                    inputs = tuple(paddle.to_tensor(inp) for inp in inputs) if isinstance(inputs, tuple) \
                        else (paddle.to_tensor(inputs), )
                    logits = self.model(*inputs)  # get logits, [bs, num_c]
                    probas = paddle.nn.functional.softmax(logits, axis=-1)  # get probabilities.
                    pred = paddle.argmax(probas, axis=-1)  # get predictions.

                    if label is None:
                        label = pred.numpy()  # label is an integer.

                    if output == 'logit':
                        return logits.numpy(), label, probas
                    else:
                        return probas.numpy(), label, probas

            self.predict_fn = predict_fn


class IntermediateLayerInterpreter(Interpreter):
    """This is one of the sub-abstract Interpreters. 
    
    :class:`IntermediateLayerInterpreter` exhibits features from intermediate layers to produce explanations.
    This interpreter extracts intermediate layers' features, but no gradients involved.
    Interpreters that are derived from :class:`IntermediateLayerInterpreter` include
    :class:`RolloutInterpreter`, :class:`ScoreCAMInterpreter`.

    This Interpreter implements :py:func:`_build_predict_fn` that returns the model's intermediate outputs given an 
    input. 
    """

    def __init__(self, model: callable, device: str, **kwargs):
        """

        Args:
            model (callable): A model with :py:func:`forward` and possibly :py:func:`backward` functions.
            device (str): The device used for running ``model``, options: ``"cpu"``, ``"gpu:0"``, ``"gpu:1"`` 
                etc.
        """

        Interpreter.__init__(self, model, device, **kwargs)
        assert hasattr(model, 'forward'), \
            "model has to be " \
            "an instance of paddle.nn.Layer or a compatible one."

    def _build_predict_fn(self, rebuild: bool = False, target_layer: str = None, target_layer_pattern: str = None):
        """Build :py:attr:`predict_fn` for IntermediateLayer based algorithms.
        The model is supposed to be a classification model.
        ``target_layer`` and ``target_layer_pattern`` cannot be set at the same time. See the arguments below.

        Args:
            rebuild (bool, optional): forces to rebuild. Defaults to ``False``.
            target_layer (str, optional): the name of the desired layer whose features will output. This is used when
                there is only one layer to output. Conflict with ``target_layer_pattern``. Defaults to ``None``.
            target_layer_pattern (str, optional): the pattern name of the layers whose features will output. This is 
                used when there are several layers to output and they share a common pattern name. Conflict with 
                ``target_layer``. Defaults to ``None``.
        """

        if self.predict_fn is not None:
            assert callable(self.predict_fn), "predict_fn is predefined before, but is not callable." \
                "Check it again."

        if self.predict_fn is None or rebuild:
            assert not (target_layer is None and target_layer_pattern is None), 'one of them must be given.'
            assert target_layer is None or target_layer_pattern is None, 'they cannot be given at the same time.'

            self._env_setup()

            def predict_fn(data):
                import paddle
                import re

                def target_layer_pattern_match(layer_name):
                    return re.match(target_layer_pattern, layer_name)

                def target_layer_match(layer_name):
                    return layer_name == target_layer

                match_func = target_layer_match if target_layer is not None else target_layer_pattern_match

                target_feature_maps = []

                def hook(layer, input, output):
                    target_feature_maps.append(output.numpy())

                hooks = []
                for name, v in self.model.named_sublayers():
                    if match_func(name):
                        h = v.register_forward_post_hook(hook)
                        hooks.append(h)

                assert len(hooks) > 0, f"No target layers are found in the given model, \
                                the list of layer names are \n \
                                {[n for n, v in self.model.named_sublayers()]}"

                with paddle.no_grad():
                    data = paddle.to_tensor(data)
                    logits = self.model(data)

                    # hooks has to be removed.
                    for h in hooks:
                        h.remove()

                    probas = paddle.nn.functional.softmax(logits, axis=1)
                    predict_label = paddle.argmax(probas, axis=1)  # get predictions.

                return target_feature_maps, probas.numpy(), predict_label.numpy()

            self.predict_fn = predict_fn

            
class TransformerInterpreter(Interpreter):
    """This is one of the sub-abstract Interpreters. 
    
    :class:`TransformerNLPInterpreter` are used by Interpreters for Transformer based model. Interpreters that are derived from 
    :class:`TransformerNLPInterpreter` include :class:`BTNLPInterpreter`, :class:`GANLPInterpreter`.

    This Interpreter implements :py:func:`_build_predict_fn` that returns servral variables and gradients in each layer. 
    """

    def __init__(self, model: callable, device: str, **kwargs):
        """
        
        Args:
            model (callable): A model with :py:func:`forward` and possibly :py:func:`backward` functions.
            device (str): The device used for running ``model``, options: ``"cpu"``, ``"gpu:0"``, ``"gpu:1"`` 
                etc.
        """
        Interpreter.__init__(self, model, device, **kwargs)
        assert hasattr(model, 'forward'), \
            "model has to be " \
            "an instance of paddle.nn.Layer or a compatible one."

    def _build_predict_fn(
            self, 
            rebuild: bool = False, 
            embedding_name: str or None = None, 
            attn_map_name: str or None = None, 
            attn_v_name: str or None = None, 
            attn_proj_name: str or None = None, 
            gradient_of: str or None = None):
        
        """Build ``predict_fn`` for transformer based algorithms.
        The model is supposed to be a classification model.

        Args:
            rebuild (bool, optional): forces to rebuild. Defaults to ``False``.
            embedding_name (str, optional): the layer name for embedding, if in need.
            attn_map_name (str, optional): the layer name for attention weights, if in need.
            attn_v_name (str, optional): the layer name for attention value.
            attn_proj_name (str, optional): the layer name for attention projection, if in need.
            nlp (bool, default to False): whether the input data is for language test.
        """

        if self.predict_fn is not None:
            assert callable(self.predict_fn), "predict_fn is predefined before, but is not callable." \
                "Check it again."

        if self.predict_fn is None or rebuild:
            self._env_setup()

            def predict_fn(inputs, label=None, scale: float or None=None):
                """predict_fn for input gradients based interpreters,
                    for image classification models only.

                Args:
                    inputs ([type]): scaled input data.
                    label ([type]): can be None.
                    scale (float, optional): noise scale for intergrated gradient and smooth gradient 

                Returns:
                    [type]: 
                """
                import paddle

                if isinstance(inputs, tuple):
                    _inputs = []
                    for inp in inputs:
                        inp = paddle.to_tensor(inp)
                        inp.stop_gradient = False
                        _inputs.append(inp)
                    inputs = tuple(_inputs)
                else:
                    inputs = paddle.to_tensor(inputs)
                    inputs.stop_gradient = False

                inputs = tuple(paddle.to_tensor(inp) for inp in inputs) if isinstance(inputs, tuple) \
                        else (paddle.to_tensor(inputs), )
                
                # when alpha is not None
                def hook(layer, input, output):
                    if scale is not None:
                        output = scale * output
                    return output

                # to obtain the attention weights
                block_attns = []
                def block_attn_hook(layer, input, output):
                    block_attns.append(output)

                # to obtain the input of each attention block
                block_inputs = []
                def block_input_hook(layer, input):
                    block_inputs.append(input)

                # to obtain the value and projection weights
                block_values = []
                def block_value_hook(layer, input, output):
                    block_values.append(output)

                # apply hooks in the forward pass
                block_projs = []
                hooks = []
                for n, v in self.model.named_sublayers():
                    if attn_map_name is not None and re.match(attn_map_name, n):
                        h = v.register_forward_post_hook(block_attn_hook)
                        hooks.append(h)
                    elif scale is not None and embedding_name is not None and re.match(embedding_name, n):
                        h = v.register_forward_post_hook(hook)
                        hooks.append(h)
                    elif attn_proj_name is not None and re.match(attn_proj_name, n):
                        block_projs.append(v.weight)
                    elif attn_v_name is not None and re.match(attn_v_name, n):
                        h = v.register_forward_pre_hook(block_input_hook)
                        hooks.append(h)
                        h = v.register_forward_post_hook(block_value_hook)
                        hooks.append(h)
                
                logits = self.model(*inputs)
                
                for h in hooks:
                    h.remove()

                proba = paddle.nn.functional.softmax(logits, axis=1)
                preds = paddle.argmax(proba, axis=1)
                if label is None:
                    label = preds.numpy()
                label_onehot = paddle.nn.functional.one_hot(paddle.to_tensor(label), num_classes=logits.shape[1])

                block_attns_grads = []

                if gradient_of == 'probability' or gradient_of is None:
                    target = paddle.sum(proba * label_onehot, axis=1)
                    target.backward()
                elif gradient_of == 'logit':
                    target = paddle.sum(logits * label_onehot, axis=1)
                    target.backward()
                else:
                    raise ValueError("`gradient_of` should be one of [logits, probability].")

                for i, attn in enumerate(block_attns):
                    grad = attn.grad.numpy()
                    block_attns_grads.append(grad)
                    block_attns[i] = attn.numpy()
                target.clear_gradient()

                for i, inp in enumerate(block_inputs):
                    block_inputs[i] = inp[0].numpy()
                
                for i, value in enumerate(block_values):
                    # check whether q,k,v are concatenated.
                    d_inp = block_inputs[i].shape[-1]
                    d_value = value.shape[-1]
                    if d_inp == d_value:
                        block_values[i] = value[0].numpy()
                    elif d_inp * 3 == d_value:
                        b, s, _ = value.shape
                        value = value.reshape((b, s, 3, -1))  # 3 == [q,k,v], b == 1.
                        block_values[i] = value[0, :, 2].numpy()
                    else:
                        raise ValueError("Report this issue to InterpretDL.")
                
                for i, proj in enumerate(block_projs):
                    block_projs[i] = proj.numpy()                
                
                return block_attns, block_attns_grads, block_inputs, block_values, block_projs, proba.numpy(), label

            self.predict_fn = predict_fn


class IntermediateGradientInterpreter(Interpreter):
    """This is one of the sub-abstract Interpreters. 
    
    :class:`IntermediateGradientInterpreter` exhibits both features and gradients from intermediate layers to produce 
    explanations. Interpreters that are derived from :class:`IntermediateGradientInterpreter` include
    :class:``, :class:``.

    This Interpreter implements :py:func:`_build_predict_fn` that returns the model's intermediate outputs given an 
    input. 
    """

    def __init__(self, model: callable, device: str = 'gpu:0') -> None:
        """
        
        Args:
            model (callable): A model with :py:func:`forward` and possibly :py:func:`backward` functions.
            device (str): The device used for running ``model``, options: ``"cpu"``, ``"gpu:0"``, ``"gpu:1"`` 
                etc.
        """
        Interpreter.__init__(self, model, device)

    def _build_predict_fn(self, rebuild=False, layer_name='word_embeddings', gradient_of='probability'):

        if self.predict_fn is not None:
            assert callable(self.predict_fn), \
                "predict_fn is predefined before, but is not callable. Check it again."
            return

        if self.predict_fn is None or rebuild:
            assert gradient_of in ['loss', 'logit', 'probability']
            self._env_setup()

            def predict_fn(inputs, label=None, scale=None, noise_amount=None):
                import paddle
                inputs = tuple(paddle.to_tensor(inp) for inp in inputs) if isinstance(inputs, tuple) \
                        else (paddle.to_tensor(inputs), )

                target_feature_map = []
                def hook(layer, input, output):
                    if scale is not None:
                        output = scale * output
                    if noise_amount is not None:
                        bias = paddle.normal(std=noise_amount * output.mean(), shape=output.shape)
                        output = output + bias
                    target_feature_map.append(output)
                    return output

                hooks = []
                for name, v in self.model.named_sublayers():
                    if layer_name in name:
                        h = v.register_forward_post_hook(hook)
                        hooks.append(h)

                logits = self.model(*inputs)   # get logits, [bs, num_c]

                for h in hooks:
                    h.remove()

                probas = paddle.nn.functional.softmax(logits, axis=1)  # get probabilities.
                preds = paddle.argmax(probas, axis=1)  # get predictions.
                if label is None:
                    label = preds.numpy()  # label is an integer.

                if gradient_of == 'loss':
                    # loss
                    loss = paddle.nn.functional.cross_entropy(logits, paddle.to_tensor(label), reduction='sum')
                else:
                    # logits or probas
                    label_onehot = paddle.nn.functional.one_hot(paddle.to_tensor(label), num_classes=probas.shape[-1])
                    if gradient_of == 'logit':
                        loss = paddle.sum(logits * label_onehot, axis=1)
                    else:
                        loss = paddle.sum(probas * label_onehot, axis=1)

                loss.backward()
                gradients = target_feature_map[0].grad
                loss.clear_gradient()

                if isinstance(gradients, paddle.Tensor):
                    gradients = gradients.numpy()

                return gradients, label, target_feature_map[0].numpy(), probas.numpy()

        self.predict_fn = predict_fn
