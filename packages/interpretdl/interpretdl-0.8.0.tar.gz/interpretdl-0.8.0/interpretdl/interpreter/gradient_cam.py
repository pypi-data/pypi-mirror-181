import numpy as np

from .abc_interpreter import Interpreter
from ..data_processor.readers import images_transform_pipeline, preprocess_save_path
from ..data_processor.visualizer import explanation_to_vis, show_vis_explanation, save_image


class GradCAMInterpreter(Interpreter):
    """
    Gradient CAM Interpreter.

    Given a convolutional network and an image classification task, classification activation map (CAM) can be derived
    from the global average pooling and the last fully-connected layer, and show the important regions that affect
    model's decisions.

    GradCAM further looks at the gradients flowing into one of the convolutional layers to give weight to activation 
    maps. Note that if there is a global average pooling layer in the network, GradCAM targeting the last layer is 
    equivalent to CAM.

    More details regarding the CAM method can be found in the original paper:
    https://arxiv.org/abs/1512.04150.

    More details regarding the GradCAM method can be found in the original paper:
    https://arxiv.org/abs/1610.02391.
    """

    def __init__(self, model: callable, device: str = 'gpu:0'):
        """
        
        Args:
            model (callable): A model with :py:func:`forward` and possibly :py:func:`backward` functions.
            device (str): The device used for running ``model``, options: ``"cpu"``, ``"gpu:0"``, ``"gpu:1"`` 
                etc.
        """
        Interpreter.__init__(self, model, device)
        self.paddle_prepared = False

        # init for usages during the interpretation.
        self._target_layer_name = None
        self._feature_maps = {}

    def interpret(self,
                  inputs: str or list(str) or np.ndarray,
                  target_layer_name: str,
                  label: list or np.ndarray = None,
                  resize_to: int = 224,
                  crop_to: int = None,
                  visual: bool = True,
                  save_path: str = None) -> np.ndarray:
        """
        The technical details of the GradCAM method are described as follows:
        GradCAM computes the feature map at the layer of ``target_layer_name`` and the gradient of the objective 
        function *w.r.t.* ``target_layer_name``. With the average of gradients along the spatial dimensions, gradients
        will be multiplied with feature map, following by a ReLU activation to produce the final explanation.

        Args:
            inputs (str or list of strs or numpy.ndarray): The input image filepath or a list of filepaths or numpy 
                array of read images.
            target_layer_name (str): The target layer to calculate gradients.
            labels (list or tuple or numpy.ndarray, optional): The target labels to analyze. 
                The number of labels should be equal to the number of images. If None, the most likely label for each
                image will be used. Default: ``None``.
            resize_to (int, optional): Images will be rescaled with the shorter edge being ``resize_to``. Defaults to 
                ``224``.
            crop_to (int, optional): After resize, images will be center cropped to a square image with the size 
                ``crop_to``. If None, no crop will be performed. Defaults to ``None``.
            visual (bool, optional): Whether or not to visualize the processed image. Default: ``True``.
            save_path (str, optional): The filepath(s) to save the processed image(s). If None, the image will not be 
                saved. Default: ``None``.

        Returns:
            [numpy.ndarray]: interpretations/heatmap for images
        """

        imgs, data = images_transform_pipeline(inputs, resize_to, crop_to)
        bsz = len(data)  # batch size
        save_path = preprocess_save_path(save_path, bsz)

        assert target_layer_name in [n for n, v in self.model.named_sublayers()], \
            f"target_layer_name {target_layer_name} does not exist in the given model, " \
            f"please check all valid layer names by [n for n, v in model.named_sublayers()]"

        if self._target_layer_name != target_layer_name:
            self._target_layer_name = target_layer_name
            self.paddle_prepared = False

        if not self.paddle_prepared:
            self._paddle_prepare()

        feature_map, gradients, preds = self.predict_fn(data, label)
        if label is None:
            label = preds

        label = np.array(label).reshape((bsz, ))
        f = np.array(feature_map.numpy())
        g = gradients

        # print(f.shape, g.shape)  # [bsz, channels, w, h]

        # the core algorithm
        cam_weights = np.mean(g, (2, 3), keepdims=True)
        heatmap = cam_weights * f
        heatmap = heatmap.mean(1)
        gradcam_explanation = np.maximum(heatmap, 0)

        # visualization and save image.
        for i in range(bsz):
            vis_explanation = explanation_to_vis(imgs[i], gradcam_explanation[i], style='overlay_heatmap')
            if visual:
                show_vis_explanation(vis_explanation)
            if save_path[i] is not None:
                save_image(save_path[i], vis_explanation)

        return gradcam_explanation

    def _paddle_prepare(self, predict_fn=None):
        if predict_fn is None:
            import paddle
            paddle.set_device(self.device)
            # to get gradients, the ``train`` mode must be set.
            # we cannot set v.training = False for the same reason.
            self.model.train()

            def hook(layer, input, output):
                self._feature_maps[layer._layer_name_for_hook] = output

            for n, v in self.model.named_sublayers():
                if n == self._target_layer_name:
                    v._layer_name_for_hook = n
                    v.register_forward_post_hook(hook)
                if "batchnorm" in v.__class__.__name__.lower():
                    v._use_global_stats = True
                if "dropout" in v.__class__.__name__.lower():
                    v.p = 0
                # Report issues or pull requests if more layers need to be added.

            def predict_fn(data, label):
                data = paddle.to_tensor(data)
                data.stop_gradient = False
                out = self.model(data)
                out = paddle.nn.functional.softmax(out, axis=1)
                preds = paddle.argmax(out, axis=1)
                if label is None:
                    label = preds.numpy()
                label_onehot = paddle.nn.functional.one_hot(paddle.to_tensor(label), num_classes=out.shape[1])
                target = paddle.sum(out * label_onehot, axis=1)

                target.backward()
                gradients = self._feature_maps[self._target_layer_name].grad
                target.clear_gradient()

                # gradients = paddle.grad(
                #     outputs=[target], inputs=[self._feature_maps])[0]
                if isinstance(gradients, paddle.Tensor):
                    gradients = gradients.numpy()

                return self._feature_maps[self._target_layer_name], gradients, label

        self.predict_fn = predict_fn
        self.paddle_prepared = True
