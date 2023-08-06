import os
import tempfile
import time
import unittest
from glob import glob

from tensorflow.keras.utils import get_file

from kolibri import ModelLoader, ModelTrainer, ModelConfig
from kolibri.data.audio import AudioFileReader
from kolibri.data.text.corpus.generators import FolderDataGenerator
from kolibri.backend.tensorflow.tasks.audio.classification import Conv1D_KapreModel
from kolibri.settings import DATA_PATH

clean_audio_root = os.path.join(get_file("audio",
                                         "https://www.dropbox.com/s/0lducehaevowqpm/test.tar.gz?dl=1",
                                         cache_dir=DATA_PATH,
                                         cache_subdir='test',
                                         untar=True), 'clean')


class TestAudio_Pipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.EPOCH_COUNT = 2
        cls.TASK_MODEL_CLASS = Conv1D_KapreModel

    def test_basic_use(self):
        confg = {'epochs': 2,
                 'delta_time': 2,
                 "batch_size": 2,
                 "save_best": True
                 }

        wav_paths = glob('{}/**'.format(clean_audio_root), recursive=True)
        wav_paths = [x.replace(os.sep, '/') for x in wav_paths if '.wav' in x]

        labels = [os.path.split(x)[0].split('/')[-1] for x in wav_paths]
        confg['pipeline'] = ['kapre_featurizer', 'dnn_audio_classifier']

        trainer = ModelTrainer(ModelConfig(confg))

        train = AudioFileReader(FolderDataGenerator(
            folder_path="/Users/mohamedmentis/Documents/Mentis/Development/Python/Hey_computer/computer/data/training/hey-computer/train",
            batch_size=4))
        test = AudioFileReader(FolderDataGenerator(
            folder_path="/Users/mohamedmentis/Documents/Mentis/Development/Python/Hey_computer/computer/data/training/hey-computer/test"))

        x_train, y_train = train.get_data()
        x_val, y_val = test.get_data()

        model = trainer.fit(x_train, y_train, x_val, y_val)

        model_path = os.path.join(tempfile.gettempdir(), str(time.time()))

        original_y = model.predict(x_train[:20])

        model_directory = trainer.persist(model_path, fixed_model_name="current")
        new_model = ModelLoader.load(model_directory)

        del model

        new_y = new_model.predict(x_train[:20])
        assert new_y == original_y


if __name__ == '__main__':
    unittest.main()
