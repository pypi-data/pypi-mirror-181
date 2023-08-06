from .abc_interpreter import Interpreter, InputGradientInterpreter
from ..data_processor.readers import images_transform_pipeline, preprocess_save_path
from ..data_processor.visualizer import explanation_to_vis, show_vis_explanation, save_image

import numpy as np


class GradShapCVInterpreter(InputGradientInterpreter):
    """
    Gradient SHAP Interpreter for CV tasks.

    For input gradient based interpreters, the target issue is generally the vanilla input gradient's noises.
    The basic idea of reducing the noises is to use different similar inputs to get the input gradients and 
    do the average. 
    
    GradShap uses noised inputs to get input gradients and then average.

    More details regarding the GradShap method can be found in the original paper:
    http://papers.nips.cc/paper/7062-a-unified-approach-to-interpreting-model-predictions.
    """

    def __init__(self, model: callable, device: str = 'gpu:0'):
        """
        
        Args:
            model (callable): A model with :py:func:`forward` and possibly :py:func:`backward` functions.
            device (str): The device used for running ``model``, options: ``"cpu"``, ``"gpu:0"``, ``"gpu:1"`` 
                etc.
        """
        InputGradientInterpreter.__init__(self, model, device)

    def interpret(self,
                  inputs: str or list(str) or np.ndarray,
                  labels: list or np.ndarray = None,
                  baselines: np.ndarray = None,
                  n_samples: int = 5,
                  noise_amount: float = 0.1,
                  gradient_of: str = 'probability',
                  resize_to: int = 224,
                  crop_to: int = None,
                  visual: bool = True,
                  save_path: str = None) -> np.ndarray:
        """The technical details of the GradShap method are described as follows:
        GradShap generates ``n_samples`` noised inputs, with the noise scale of ``noise_amount``, and then computes 
        the gradients *w.r.t.* these noised inputs. A difference between ``baselines`` and noised inputs is considered.
        The final explanation is the multiplication between the gradients and the difference to ``baselines``.

        Args:
            inputs (str or list): The input image filepath or a list of filepaths or numpy array of read images.
            labels (list or np.ndarray, optional): The target labels to analyze. The number of labels should be equal 
                to the number of images. If None, the most likely label for each image will be used. Default: ``None``.
            baselines (np.ndarray, optional): The baseline images to compare with. It should have the same shape as 
                images and same length as the number of images. If None, the baselines of all zeros will be used. 
                Default: ``None``.
            n_samples (int, optional): The number of randomly generated samples. Defaults to ``5``.
            noise_amount (float, optional): Noise level of added noise to each image. The std of Gaussian random noise
                is ``noise_amount`` * (x :sub:`max` - x :sub:`min`). Default: ``0.1``.
            gradient_of (str, optional): compute the gradient of ['probability', 'logit' or 'loss']. Default: 
                ``'probability'``. SmoothGrad uses probability for all tasks by default.
            resize_to (int, optional): Images will be rescaled with the shorter edge being ``resize_to``. Defaults to 
                ``224``.
            crop_to (int, optional): After resize, images will be center cropped to a square image with the size 
                ``crop_to``. If None, no crop will be performed. Defaults to ``None``.
            visual (bool, optional): Whether or not to visualize the processed image. Default: ``True``.
            save_path (str, optional): The filepath(s) to save the processed image(s). If None, the image will not be 
                saved. Default: ``None``.

        Returns:
            np.ndarray: the explanation result.
        """

        imgs, data = images_transform_pipeline(inputs, resize_to, crop_to)
        bsz = len(data)
        self.data_type = np.array(data).dtype

        self._build_predict_fn(gradient_of=gradient_of)

        _, predicted_label, predicted_proba = self.predict_fn(data, labels)
        self.predicted_label = predicted_label
        self.predicted_proba = predicted_proba
        if labels is None:
            labels = predicted_label

        def add_noise_to_inputs(data):
            max_axis = tuple(np.arange(1, data.ndim))
            stds = noise_amount * (np.max(data, axis=max_axis) - np.min(data, axis=max_axis))
            noise = np.concatenate([
                np.random.normal(0.0, stds[j], (n_samples, ) + tuple(d.shape)) for j, d in enumerate(data)
            ]).astype(self.data_type)
            repeated_data = np.repeat(data, (n_samples, ) * len(data), axis=0)
            return repeated_data + noise

        data_with_noise = add_noise_to_inputs(data)

        if baselines is None:
            baselines = np.zeros_like(data)
        baselines = np.repeat(baselines, (n_samples, ) * bsz, axis=0)

        labels = np.array(labels).reshape((bsz, 1))  #.repeat(n_samples, axis=0)
        labels = np.repeat(labels, (n_samples, ) * bsz, axis=0)

        rand_scales = np.random.uniform(0.0, 1.0, (bsz * n_samples, 1)).astype(self.data_type)

        input_baseline_points = np.array(
            [d * r + b * (1 - r) for d, r, b in zip(data_with_noise, rand_scales, baselines)])

        gradients, _, _ = self.predict_fn(input_baseline_points, labels)

        input_baseline_diff = data_with_noise - baselines
        explanations = gradients * input_baseline_diff

        explanations = np.concatenate(
            [np.mean(explanations[i * n_samples:(i + 1) * n_samples], axis=0, keepdims=True) for i in range(bsz)])

        # visualization and save image.
        save_path = preprocess_save_path(save_path, bsz)
        for i in range(bsz):
            vis_explanation = explanation_to_vis(imgs[i], np.abs(explanations[i]).sum(0), style='overlay_grayscale')
            if visual:
                show_vis_explanation(vis_explanation)
            if save_path[i] is not None:
                save_image(save_path[i], vis_explanation)

        return explanations


class GradShapNLPInterpreter(Interpreter):
    """
    TODO: Inherit from a subabstract interpreter.
    Gradient SHAP Interpreter for NLP tasks.

    For input gradient based interpreters, the target issue is generally the vanilla input gradient's noises.
    The basic idea of reducing the noises is to use different similar inputs to get the input gradients and 
    do the average. 

    The inputs for NLP tasks are considered as the embedding features. So the noises or the changes of inputs
    are done for the embeddings.

    More details regarding the GradShap method can be found in the original paper:
    http://papers.nips.cc/paper/7062-a-unified-approach-to-interpreting-model-predictions.
    """

    def __init__(self, model: callable, device: str = 'gpu:0') -> None:
        """
        
        Args:
            model (callable): A model with :py:func:`forward` and possibly :py:func:`backward` functions.
            device (str): The device used for running ``model``, options: ``"cpu"``, ``"gpu:0"``, ``"gpu:1"`` 
                etc.
        """
        Interpreter.__init__(self, model, device)

    def interpret(self,
                  data: tuple or np.ndarray,
                  labels: list or np.ndarray = None,
                  n_samples: int = 5,
                  noise_amount: float = 0.1,
                  embedding_name: str = 'word_embeddings',
                  return_pred: bool = True) -> np.ndarray or tuple:
        """The technical details of the GradShap method for NLP tasks are similar for CV tasks, except the noises are
        added on the embeddings.

        Args:
            data (tupleornp.ndarray): The inputs to the NLP model.
            labels (listornp.ndarray, optional): The target label to analyze. If None, the most likely label will be 
                used. Default: ``None``.
            n_samples (int, optional): The number of randomly generated samples. Defaults to ``5``.
            noise_amount (float, optional): Noise level of added noise to the embeddings. The std of Gaussian random
                noise is ``noise_amount`` * ``embedding.mean()`` * (x :sub:`max` - x :sub:`min`). Default: ``0.1``.
            embedding_name (str, optional): name of the embedding layer at which the noises will be applied. 
                The name of embedding can be verified through ``print(model)``. Defaults to ``word_embeddings``. 
            return_pred (bool, optional): Whether or not to return predicted labels and probabilities. 
                If True, a tuple of predicted labels, probabilities, and interpretations will be returned.
                There are useful for visualization. Else, only interpretations will be returned. Default: ``True``.

        Returns:
            np.ndarray or tuple: explanations, or (explanations, pred).
        """

        self._build_predict_fn(embedding_name=embedding_name)

        if isinstance(data, tuple):
            bs = data[0].shape[0]
        else:
            bs = data.shape[0]

        gradients, labels, data_out, probas = self.predict_fn(data, labels, None)
        self.predicted_label = labels
        self.predicted_proba = probas

        labels = labels.reshape((bs, ))
        total_gradients = np.zeros_like(gradients)

        rand_scales = np.random.uniform(0.0, 1.0, (n_samples, ))

        for scale in rand_scales:
            gradients, _, _, _ = self.predict_fn(data, labels, scale, noise_amount)
            total_gradients += np.array(gradients)

        interpretations = total_gradients * data_out / n_samples
        interpretations = np.sum(interpretations, axis=-1)

        # Visualization is currently not supported here.
        # See the tutorial for more information:
        # https://github.com/PaddlePaddle/InterpretDL/blob/master/tutorials/ernie-2.0-en-sst-2.ipynb
        if return_pred:
            return labels, probas.numpy(), interpretations

        return interpretations

    def _build_predict_fn(self, rebuild=False, embedding_name='word_embeddings'):

        if self.predict_fn is not None:
            assert callable(self.predict_fn), "predict_fn is predefined before, but is not callable." \
                "Check it again."
            return

        import paddle
        if self.predict_fn is None or rebuild:

            self._paddle_env_setup()

            def predict_fn(data, labels, scale=None, noise_amount=None):
                if isinstance(data, tuple):
                    # NLP models usually have two inputs.
                    bs = data[0].shape[0]
                    data = (paddle.to_tensor(data[0]), paddle.to_tensor(data[1]))
                else:
                    bs = data.shape[0]
                    data = paddle.to_tensor(data)

                assert labels is None or \
                    (isinstance(labels, (list, np.ndarray)) and len(labels) == bs)

                target_feature_map = []

                def hook(layer, input, output):
                    if noise_amount is not None:
                        bias = paddle.normal(std=noise_amount * output.mean(), shape=output.shape)
                        output = output + bias
                    if scale is not None:
                        output = scale * output
                    target_feature_map.append(output)
                    return output

                hooks = []
                for name, v in self.model.named_sublayers():
                    if embedding_name in name:
                        h = v.register_forward_post_hook(hook)
                        hooks.append(h)

                if isinstance(data, tuple):
                    logits = self.model(*data)  # get logits, [bs, num_c]
                else:
                    logits = self.model(data)  # get logits, [bs, num_c]

                for h in hooks:
                    h.remove()

                probas = paddle.nn.functional.softmax(logits, axis=1)  # get probabilities.
                preds = paddle.argmax(probas, axis=1)  # get predictions.
                if labels is None:
                    labels = preds.numpy()  # label is an integer.

                # logits or probas
                labels = np.array(labels).reshape((bs, ))
                labels_onehot = paddle.nn.functional.one_hot(paddle.to_tensor(labels), num_classes=probas.shape[1])
                loss = paddle.sum(probas * labels_onehot, axis=1)

                loss.backward()
                gradients = target_feature_map[0].grad  # get gradients of "embedding".
                loss.clear_gradient()

                if isinstance(gradients, paddle.Tensor):
                    gradients = gradients.numpy()
                return gradients, labels, target_feature_map[0].numpy(), probas

        self.predict_fn = predict_fn
