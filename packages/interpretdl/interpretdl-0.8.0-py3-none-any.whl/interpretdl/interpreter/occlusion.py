from tqdm import tqdm
import numpy as np

from .abc_interpreter import Interpreter, InputOutputInterpreter
from ..data_processor.readers import images_transform_pipeline, preprocess_save_path
from ..data_processor.visualizer import explanation_to_vis, show_vis_explanation, save_image


class OcclusionInterpreter(InputOutputInterpreter):
    """
    Occlusion Interpreter.

    OcclusionInterpreter follows the simple idea of perturbation that says if the most important input features are
    perturbed, then the model's prediction will change the most. OcclusionInterpreter masks a block of pixels in the
    image, and then computes the prediction changes. According to the changes, the final explanation is obtained. 

    More details regarding the Occlusion method can be found in the original paper:
    https://arxiv.org/abs/1311.2901

    Part of the code is modified from https://github.com/pytorch/captum/blob/master/captum/attr/_core/occlusion.py.
    """

    def __init__(self, model: callable, device: str = 'gpu:0') -> None:
        """
        
        Args:
            model (callable): A model with :py:func:`forward` and possibly :py:func:`backward` functions.
            device (str): The device used for running ``model``, options: ``"cpu"``, ``"gpu:0"``, ``"gpu:1"`` 
                etc.
        """
        InputOutputInterpreter.__init__(self, model, device)

    def interpret(self,
                  inputs: str,
                  sliding_window_shapes: tuple,
                  labels: int or None = None,
                  strides: int = 1,
                  baselines: np.ndarray or None = None,
                  perturbations_per_eval: int = 1,
                  resize_to: int = 224,
                  crop_to: int or None = None,
                  visual: bool = True,
                  save_path: str = None):
        """
        Part of the code is modified from https://github.com/pytorch/captum/blob/master/captum/attr/_core/occlusion.py.

        Args:
            inputs (str or list of strs or numpy.ndarray): The input image filepath or a list of filepaths or numpy 
                array of read images.
            sliding_window_shapes (tuple): Shape of sliding windows to occlude data.
            labels (list or tuple or numpy.ndarray, optional): The target labels to analyze. The number of labels 
                should be equal to the number of images. If None, the most likely label for each image will be used. 
                Default: None
            strides (int or tuple): The step by which the occlusion should be shifted by in each direction for each 
                iteration. If int, the step size in each direction will be the same. Default: ``1``.
            baselines (numpy.ndarray or None, optional): The baseline images to compare with. It should have the same
                shape as images. If None, the baselines of all zeros will be used. Default: ``None``.
            perturbations_per_eval (int, optional): number of occlusions in each batch. Default: ``1``.
            resize_to (int, optional): Images will be rescaled with the shorter edge being ``resize_to``. Defaults to 
                ``224``.
            crop_to (int, optional): After resize, images will be center cropped to a square image with the size 
                ``crop_to``. If None, no crop will be performed. Defaults to ``None``.
            visual (bool, optional): Whether or not to visualize the processed image. Default: ``True``.
            save_path (str, optional): The filepath(s) to save the processed image(s). If None, the image will not be 
                saved. Default: ``None``.

        Returns:
            [numpy.ndarray]: interpretations for images
        """

        imgs, data = images_transform_pipeline(inputs, resize_to, crop_to)

        bsz = len(data)
        save_path = preprocess_save_path(save_path, bsz)

        self._build_predict_fn(output='probability')

        if baselines is None:
            baselines = np.zeros_like(data)
        elif np.array(baselines).ndim == 3:
            baselines = np.repeat(np.expand_dims(baselines, 0), len(data), 0)
        if len(baselines) == 1:
            baselines = np.repeat(baselines, len(data), 0)

        probas, label, _ = self.predict_fn(data, None)
        self.predicted_label = labels
        self.predicted_proba = probas

        sliding_windows = np.ones(sliding_window_shapes)

        if labels is None:
            labels = np.argmax(probas, axis=1)
        elif isinstance(labels, int):
            labels = [labels]

        img_size = [3, crop_to, crop_to] if crop_to is not None else [3, imgs.shape[1], imgs.shape[2]]
        current_shape = np.subtract(img_size, sliding_window_shapes)
        shift_counts = tuple(np.add(np.ceil(np.divide(current_shape, strides)).astype(int), 1))

        initial_eval = np.array([probas[i][labels[i]] for i in range(bsz)]).reshape((1, bsz))
        total_interp = np.zeros_like(data)

        num_features = np.prod(shift_counts)
        with tqdm(total=num_features, leave=True, position=0) as pbar:
            for (ablated_features, current_mask) in self._ablation_generator(data, sliding_windows, strides, baselines,
                                                                             shift_counts, perturbations_per_eval):
                ablated_features = ablated_features.reshape((-1, ) + ablated_features.shape[2:])
                modified_probs, _, _ = self.predict_fn(np.float32(ablated_features), None)
                modified_eval = [p[labels[i % bsz]] for i, p in enumerate(modified_probs)]
                eval_diff = initial_eval - np.array(modified_eval).reshape((-1, bsz))
                eval_diff = eval_diff.T
                dim_tuple = (len(current_mask), ) + (1, ) * (current_mask.ndim - 1)
                for i, diffs in enumerate(eval_diff):
                    #j = i % perturbations_per_eval
                    total_interp[i] += np.sum(diffs.reshape(dim_tuple) * current_mask, axis=0)[0]

                pbar.update(1)

        # visualization and save image.
        for i in range(len(data)):
            vis_explanation = explanation_to_vis(imgs[i], np.abs(total_interp[i]).sum(0), style='overlay_grayscale')
            if visual:
                show_vis_explanation(vis_explanation)
            if save_path[i] is not None:
                save_image(save_path[i], vis_explanation)

        return total_interp

    def _ablation_generator(self, inputs, sliding_window, strides, baselines, shift_counts, perturbations_per_eval):
        num_features = np.prod(shift_counts)
        perturbations_per_eval = min(perturbations_per_eval, num_features)
        num_features_processed = 0
        num_examples = len(inputs)
        if perturbations_per_eval > 1:
            all_features_repeated = np.repeat(np.expand_dims(inputs, 0), perturbations_per_eval, axis=0)
        else:
            all_features_repeated = np.expand_dims(inputs, 0)

        while num_features_processed < num_features:
            current_num_ablated_features = min(perturbations_per_eval, num_features - num_features_processed)
            if current_num_ablated_features != perturbations_per_eval:
                current_features = all_features_repeated[:current_num_ablated_features]
            else:
                current_features = all_features_repeated

            ablated_features, current_mask = self._construct_ablated_input(
                current_features, baselines, num_features_processed,
                num_features_processed + current_num_ablated_features, sliding_window, strides, shift_counts)

            yield ablated_features, current_mask
            num_features_processed += current_num_ablated_features

    def _construct_ablated_input(self, inputs, baselines, start_feature, end_feature, sliding_window, strides,
                                 shift_counts):
        input_masks = np.array([
            self._occlusion_mask(inputs, j, sliding_window, strides, shift_counts)
            for j in range(start_feature, end_feature)
        ])
        ablated_tensor = inputs * (1 - input_masks) + baselines * input_masks

        return ablated_tensor, input_masks

    def _occlusion_mask(self, inputs, ablated_feature_num, sliding_window, strides, shift_counts):
        remaining_total = ablated_feature_num

        current_index = []
        for i, shift_count in enumerate(shift_counts):
            stride = strides[i] if isinstance(strides, tuple) else strides
            current_index.append((remaining_total % shift_count) * stride)
            remaining_total = remaining_total // shift_count

        remaining_padding = np.subtract(inputs.shape[2:], np.add(current_index, sliding_window.shape))

        slicers = []
        for i, p in enumerate(remaining_padding):
            # When there is no enough space for sliding window, truncate the window
            if p < 0:
                slicer = [slice(None)] * len(sliding_window.shape)
                slicer[i] = range(sliding_window.shape[i] + p)
                slicers.append(slicer)

        pad_values = tuple(tuple(reversed(np.maximum(pair, 0))) for pair in zip(remaining_padding, current_index))

        for slicer in slicers:
            sliding_window = sliding_window[tuple(slicer)]
        padded = np.pad(sliding_window, pad_values)

        return padded.reshape((1, ) + padded.shape)
