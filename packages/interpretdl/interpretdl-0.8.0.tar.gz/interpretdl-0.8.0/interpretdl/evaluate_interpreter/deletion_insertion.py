import numpy as np
import cv2
from .abc_evaluator import InterpreterEvaluator
from ..data_processor.readers import images_transform_pipeline, preprocess_image


class DeletionInsertion(InterpreterEvaluator):
    """
    Deletion & Insertion Interpreter Evaluation method. 

    The evaluation of interpretation algorithms follows the intuition that flipping the most salient pixels first 
    should lead to high performance decay. Perturbation-based examples can therefore be used for the trustworthiness
    evaluations of interpretation algorithms. 

    The Deletion metric is computed as follows. The perturbation starts from an original image, perturbs (zeros 
    out) the most important pixels in the input, and then computes the responses of the trained model. So that a 
    curve, with ratios of perturbed pixels as x-axis and probabilities as y-axis, can be obtained and the area under
    this curve is the deletion score.

    The Insertion metric is similar, but the perturbation starts from a zero image, inserts the most important pixels
    to the input, and then computes the responses of the trained model. A similar curve can be obtained and the area 
    under this curve is the insertion score.

    More details regarding the Deletion & Insertion method can be found in the original paper:
    https://arxiv.org/abs/1806.07421
    """

    def __init__(self,
                 model: callable,
                 device: str,
                 compute_deletion: bool = True,
                 compute_insertion: bool = True,
                 **kwargs):
        """

        Args:
            model (callable): A model with :py:func:`forward` and possibly :py:func:`backward` functions. This 
                is not always required if the model is not involved. 
            device (str): The device used for running ``model``, options: ``"cpu"``, ``"gpu:0"``, ``"gpu:1"`` 
                etc. Again, this is not always required if the model is not involved.
            compute_deletion (bool, optional): Whether compute deletion score. Defaults to ``True``.
            compute_insertion (bool, optional): Whether compute insertion score. Defaults to ``True``.

        Raises:
            ValueError: At least one of ``compute_deletion`` and ``compute_insertion`` must be True.
        """
        super().__init__(model, device, **kwargs)

        if (not compute_deletion) or (not compute_insertion):
            raise ValueError('At least one of ``compute_deletion`` and ``compute_insertion`` must be True.')
        self.compute_deletion = compute_deletion
        self.compute_insertion = compute_insertion
        self.evaluate_lime = False

        self._build_predict_fn()

    def evaluate(self,
                 img_path: str,
                 explanation: dict or np.ndarray,
                 batch_size: int or None = None,
                 resize_to: int = 224,
                 crop_to: int or None = None,
                 limit_number_generated_samples: int or None = None) -> dict:
        """Given ``img_path``, DeletionInsertion first generates perturbed samples of deletion and insertion,
        respectively, according to the order provided by ``explanation``. The number of samples is defined by 
        ``limit_number_generated_samples`` (a sampling is used for the numbers are different). Then DeletionInsertion
        computes the probabilities of these perturbed samples, and the mean of all probabilities of the class of 
        interest is computed for the final score.

        Note that LIME produces explanations based on superpixels, the number of perturbed samples is originally equal
        to the number of superpixels. So if ``limit_number_generated_samples`` is None, then the number of superpixels
        is used. For other explanations that produce the explanation of the same spatial dimension as the input image,
        ``limit_number_generated_samples`` is set to ``20`` if not given.

        Args:
            img_path (str): a string for image path.
            explanation (dict or np.ndarray): the explanation result from an interpretation algorithm.
            batch_size (int or None, optional): batch size for each pass. Defaults to ``None``.
            resize_to (int, optional): Images will be rescaled with the shorter edge being ``resize_to``. Defaults to 
                ``224``.
            crop_to (int, optional): After resize, images will be center cropped to a square image with the size 
                ``crop_to``. If None, no crop will be performed. Defaults to ``None``.
            limit_number_generated_samples (int or None, optional): a maximum value for samples of perturbation. If 
                None, it will be automatically chosen. The number of superpixels is used for LIME explanations, 
                otherwise, ``20`` is to be set. Defaults to ``None``.

        Returns:
            dict: 
                A dict containing ``'deletion_score'``, ``'del_probas'``, ``'deletion_images'``, ``'insertion_score'``,
                ``'ins_probas'`` and ``'insertion_images'``, if ``compute_deletion`` and ``compute_insertion``
                are both True.
        """

        if not isinstance(explanation, np.ndarray):
            # if not an array, then should be lime results.
            # for lime results, superpixel segmentation corresponding to the lime_weights is required.
            assert isinstance(explanation, dict) and 'segmentation' in explanation, \
                'For LIME results, give the LIMECVInterpreter.lime_results as explanation. ' \
                'If there are confusions, please contact us.'
            self.evaluate_lime = True

        results = {}
        if self.compute_deletion:
            results['deletion_score'] = 0.0
            results['del_probas'] = None
        if self.compute_insertion:
            results['insertion_score'] = 0.0
            results['ins_probas'] = None

        img, _ = images_transform_pipeline(img_path, resize_to=resize_to, crop_to=crop_to)
        results = self.generate_samples(img, explanation, limit_number_generated_samples, results)
        results = self.compute_probas(results, batch_size)

        return results

    def generate_samples(self, img, explanation, limit_number_generated_samples, results):

        if self.evaluate_lime:
            return self.generate_samples_lime(img, explanation, limit_number_generated_samples, results)
        else:
            return self.generate_samples_array(img, explanation, limit_number_generated_samples, results)

    def generate_samples_lime(self, img, explanation, limit_number_generated_samples, results):
        sp_segments = explanation['segmentation']
        lime_weights = explanation['lime_weights']
        interpret_class = list(lime_weights.keys())[0]

        if self.compute_deletion:
            deletion_images = [img]
            sp_order = [sp for sp, v in lime_weights[interpret_class]]
            fudged_image = img.copy()
            mx = (127, 127, 127)
            for sp in sp_order:
                fudged_image = fudged_image.copy()

                indices = np.where(sp_segments == sp)
                fudged_image[:, indices[0], indices[1]] = mx

                deletion_images.append(fudged_image)

            if limit_number_generated_samples is not None and limit_number_generated_samples < len(deletion_images):
                indices = np.linspace(0, len(deletion_images) - 1, limit_number_generated_samples).astype(np.int32)
                deletion_images = [deletion_images[i] for i in indices]

            deletion_images = np.vstack(deletion_images)
            results['deletion_images'] = deletion_images

        if self.compute_insertion:
            insertion_images = []
            sp_order = [sp for sp, v in lime_weights[interpret_class]]
            fudged_image = np.zeros_like(img) + 127
            for sp in sp_order:
                fudged_image = fudged_image.copy()

                indices = np.where(sp_segments == sp)
                fudged_image[:, indices[0], indices[1]] = img[:, indices[0], indices[1]]

                insertion_images.append(fudged_image)

            insertion_images.append(img)

            if limit_number_generated_samples is not None and limit_number_generated_samples < len(insertion_images):
                indices = np.linspace(0, len(insertion_images) - 1, limit_number_generated_samples).astype(np.int32)
                insertion_images = [insertion_images[i] for i in indices]

            insertion_images = np.vstack(insertion_images)
            results['insertion_images'] = insertion_images

        return results

    def generate_samples_array(self, img, explanation, limit_number_generated_samples, results):

        # usually explanation has shape of [n_sample, n_channel, h, w]
        explanation = np.squeeze(explanation)
        assert len(explanation.shape) in [2, 3], 'Explanation for one image.'
        if len(explanation.shape) == 3:
            explanation = np.abs(explanation).sum(0)
        assert len(explanation.shape) == 2

        explanation = cv2.resize(explanation, (img.shape[2], img.shape[1]), interpolation=cv2.INTER_LINEAR)

        if limit_number_generated_samples is None:
            limit_number_generated_samples = 20  # default to 20, each 5 percentiles.

        q = 100. / limit_number_generated_samples
        qs = [q * (i - 1) for i in range(limit_number_generated_samples, 0, -1)]
        percentiles = np.percentile(explanation, qs)

        if self.compute_deletion:
            deletion_images = [img]

            fudged_image = img.copy()
            for p in percentiles:
                fudged_image = fudged_image.copy()
                mx = (127, 127, 127)
                indices = np.where(explanation > p)
                fudged_image[:, indices[0], indices[1]] = mx
                deletion_images.append(fudged_image)
            deletion_images = np.vstack(deletion_images)
            results['deletion_images'] = deletion_images

        if self.compute_insertion:
            insertion_images = []
            fudged_image = np.zeros_like(img) + 127
            for p in percentiles:
                fudged_image = fudged_image.copy()
                indices = np.where(explanation > p)
                fudged_image[:, indices[0], indices[1]] = img[:, indices[0], indices[1]]
                insertion_images.append(fudged_image)
            insertion_images.append(img)

            insertion_images = np.vstack(insertion_images)
            results['insertion_images'] = insertion_images

        return results

    def compute_probas(self, results, batch_size, coi=None):
        if self.compute_deletion:
            data = preprocess_image(results['deletion_images'])
            if batch_size is None:
                probas = self.predict_fn(data)
            else:
                probas = []
                list_to_compute = list(range(data.shape[0]))
                while len(list_to_compute) > 0:
                    if len(list_to_compute) >= batch_size:
                        list_c = list_to_compute[:batch_size]
                        list_to_compute = list_to_compute[batch_size:]
                    else:
                        list_c = list_to_compute[:len(list_to_compute)]
                        list_to_compute = []

                    probs_batch = self.predict_fn(data[list_c])
                    probas.append(probs_batch)

                probas = np.concatenate(probas, axis=0)

            # class of interest
            if coi is None:
                # probas.shape = [n_samples, n_classes]
                coi = np.argmax(probas[0], axis=0)

            results['del_probas'] = probas[:, coi]
            results['deletion_score'] = np.mean(results['del_probas'])

        if self.compute_insertion:
            data = preprocess_image(results['insertion_images'])
            if batch_size is None:
                probas = self.predict_fn(data)
            else:
                probas = []
                list_to_compute = list(range(data.shape[0]))
                while len(list_to_compute) > 0:
                    if len(list_to_compute) >= batch_size:
                        list_c = list_to_compute[:batch_size]
                        list_to_compute = list_to_compute[batch_size:]
                    else:
                        list_c = list_to_compute[:len(list_to_compute)]
                        list_to_compute = []

                    probs_batch = self.predict_fn(data[list_c])
                    probas.append(probs_batch)

                probas = np.concatenate(probas, axis=0)

            # class of interest
            if coi is None:
                # probas.shape = [n_samples, n_classes]
                coi = np.argmax(probas[-1], axis=0)

            results['ins_probas'] = probas[:, coi]
            results['insertion_score'] = np.mean(results['ins_probas'])

        return results
