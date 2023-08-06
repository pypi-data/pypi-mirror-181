import numpy as np
import paddle

from .lime import LIMECVInterpreter
from ._lime_base import compute_segments
from ._global_prior_base import precompute_global_prior, cluster_global_weights_to_local_prior
from ..data_processor.readers import preprocess_image, read_image, restore_image
from ..data_processor.readers import load_npy_dict_file
from ..data_processor.visualizer import sp_weights_to_image_explanation, overlay_threshold, save_image, show_vis_explanation


class LIMEPriorInterpreter(LIMECVInterpreter):
    """
    LIME Prior Interpreter. This is an Interpreter in progress.

    Depreciated. Refer to GLIMECVInterpreter.
    """

    def __init__(self,
                 model: callable,
                 prior_method: str = "none",
                 device: str = 'gpu:0') -> None:
        """

        Args:
            model (callable): A model with :py:func:`forward` and possibly :py:func:`backward` functions.
            prior_method: Prior method. Can be chosen from ``{"none", "ridge"}``. Defaults to ``"none"``, which is 
                equivalent to LIME. If ``none``, :py:func:`interpret()` will use zeros as prior; Otherwise, the loaded
                prior will be used.
            device (str): The device used for running ``model``, options: ``"cpu"``, ``"gpu:0"``, ``"gpu:1"`` 
                etc.
        """
        LIMECVInterpreter.__init__(self, model, device)
        self.prior_method = prior_method
        self.global_weights = None

    def interpreter_init(self, list_file_paths=None, batch_size=0, weights_file_path=None):
        """
        Pre-compute global weights.

        If ``weights_file_path`` is given and has contents, then skip the pre-compute process and
        read the content as the global weights; else the pre-compute process should be performed
        with `list_file_paths`. After the pre-compute process, if `weights_file_path` is given,
        then the prec-computed weights will be saved in this path for skipping the pre-compute
        process in the next usage.
        This is an additional step that LIMEPrior Interpreter has to perform before interpretation.

        Args:
            list_file_paths: List of files used to compute the global prior.
            batch_size: Number of samples to forward each time.
            weights_file_path: Path to load as prior.

        Returns:
            None.

        """

        assert list_file_paths is not None or weights_file_path is not None, \
            "Cannot prepare without anything. "

        self._build_predict_fn(rebuild=True, output='probability')

        def predict_fn_for_lime(_imgs):
            _data = preprocess_image(_imgs)  # transpose to [N, 3, H, W], scaled to [0.0, 1.0]

            output, _, _ = self.predict_fn(_data, None)
            return output

        self.predict_fn_for_lime = predict_fn_for_lime

        precomputed_weights = load_npy_dict_file(weights_file_path)
        if precomputed_weights is not None:
            self.global_weights = precomputed_weights
        else:
            self.global_weights = precompute_global_prior(list_file_paths, self.predict_fn_for_lime, batch_size,
                                                          self.prior_method)
            if weights_file_path is not None and self.global_weights is not None:
                np.save(weights_file_path, self.global_weights)

    def interpret(self,
                  data: str,
                  interpret_class: int or None = None,
                  prior_reg_force: float = 1.0,
                  num_samples: int = 1000,
                  batch_size: int = 50,
                  resize_to: int = 224,
                  crop_to: int = None,
                  visual: bool = True,
                  save_path: str = None):
        """
        Note that for LIME prior interpreter, :py:func:`interpreter_init()` needs to be called before calling 
        :py:func:`interpret()`.

        Args:
            data (str): The input file path.
            interpret_class (int, optional): The index of class to interpret. If None, the most likely label will be 
                used. Default: ``None``.
            prior_reg_force (float, optional): The regularization force to apply. Default: ``1.0``.
            num_samples (int, optional): LIME sampling numbers. Larger number of samples usually gives more accurate 
                interpretation. Default: ``1000``.
            batch_size (int, optional): Number of samples to forward each time. Default: 50
            resize_to (int, optional): Images will be rescaled with the shorter edge being ``resize_to``. Defaults to
                ``224``.
            crop_to ([type], optional): After resize, images will be center cropped to a square image 
                with the size ``crop_to``. If None, no crop will be performed. Defaults to ``None``.
            visual (bool, optional): Whether or not to visualize the processed image. Default: ``True``.
            save_path (str, optional): The path to save the processed image. If None, the image will not be saved. 
                Default: ``None``.

        Returns:
            [dict]: LIME results: {interpret_label_i: weights on features}

        """
        if self.global_weights is None and self.prior_method != "none":
            raise ValueError("The interpreter is not prepared. Call prepare() before interpretation.")

        # preprocess_input
        if isinstance(data, str):
            img = read_image(data, resize_to, crop_to)
        else:
            if len(data.shape) == 3:
                data = np.expand_dims(data, axis=0)
            if np.issubdtype(data.dtype, np.integer):
                img = data
            else:
                # for later visualization
                img = restore_image(data.copy())
        data = preprocess_image(img)

        self._build_predict_fn(output='probability')

        probability, _, _ = self.predict_fn(data, None)
        probability = probability[0]  # only one example here

        if interpret_class is None:
            # only interpret top 1 if not provided.
            pred_label = np.argsort(probability)
            interpret_class = pred_label[-1:]
            interpret_class = np.array(interpret_class)
        elif isinstance(interpret_class, list):
            interpret_class = np.array(interpret_class)
        else:
            interpret_class = np.array([interpret_class])

        # def predict_fn_for_lime(_imgs):
        #     _data = preprocess_image(
        #         _imgs
        #     )  # transpose to [N, 3, H, W], scaled to [0.0, 1.0]

        #     output, _ = self.predict_fn(_data, None)
        #     return output

        # self.predict_fn_for_lime = predict_fn_for_lime
        if self.lime_base.segments is None:
            self.lime_base.segments = compute_segments(img[0])

        segments = self.lime_base.segments

        if self.prior_method == "none":
            prior = np.zeros(len(np.unique(segments)))
        else:
            prior = cluster_global_weights_to_local_prior(img, segments, interpret_class[0], self.global_weights)

        lime_weights, r2_scores = self.lime_base.interpret_instance(img[0],
                                                                    self.predict_fn_for_lime,
                                                                    interpret_class,
                                                                    num_samples=num_samples,
                                                                    batch_size=batch_size,
                                                                    prior=prior,
                                                                    reg_force=prior_reg_force)

        # visualization and save image.
        explanation_mask = sp_weights_to_image_explanation(img[0], lime_weights, interpret_class[0],
                                                           self.lime_base.segments)
        explanation_vis = overlay_threshold(img[0], explanation_mask)
        if visual:
            show_vis_explanation(explanation_vis)
        if save_path is not None:
            save_image(save_path, explanation_vis)

        self.lime_results['probability'] = probability
        self.lime_results['input'] = img[0]
        self.lime_results['segmentation'] = self.lime_base.segments
        self.lime_results['r2_scores'] = r2_scores
        self.lime_results['lime_weights'] = lime_weights

        return lime_weights
