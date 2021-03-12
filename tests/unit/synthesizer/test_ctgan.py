from unittest import TestCase

import pandas as pd
import pytest
import torch

from ctgan.synthesizers.ctgan import CTGANSynthesizer, Discriminator, Generator, Residual


class TestDiscriminator(TestCase):

    def test___init__(self):
        """Test `__init__` for a generic case.

        Make sure 'self.seq' has same length as 3*`discriminator_dim` + 1.

        Setup:
            - Create Discriminator

        Input:
            - input_dim = positive integer
            - discriminator_dim = list of integers
            - pack = positive integer

        Output:
            - None

        Side Effects:
            - Set `self.seq`, `self.pack` and `self.packdim`
        """
        discriminator_dim = [1, 2, 3]
        discriminator = Discriminator(input_dim=50, discriminator_dim=discriminator_dim, pac=7)

        assert discriminator.pac == 7
        assert discriminator.pacdim == 350
        assert len(discriminator.seq) == 3 * len(discriminator_dim) + 1

    def test_forward(self):
        """Test `test_forward` for a generic case.

        Check that the output shapes are correct.
        We can also test that all parameters have a gradient attached to them
        by running `encoder.parameters()`. To do that, we just need to use `loss.backward()`
        for some loss, like `loss = torch.mean(output)`. Notice that the input_dim = input_size.

        Setup:
            - initialize with input_size, discriminator_dim, pac
            - Create random tensor as input

        Input:
            - input = random tensor of shape (N, input_size)

        Output:
            - tensor of shape (N/pac, 1)
        """
        discriminator = Discriminator(input_dim=50, discriminator_dim=[100, 200, 300], pac=7)
        output = discriminator(torch.randn(70, 50))
        assert output.shape == (10, 1)

        # Check to make sure no gradients attached
        for parameter in discriminator.parameters():
            assert parameter.grad is None

        # Backpropagate
        output.mean().backward()

        # Check to make sure all parameters have gradients
        for parameter in discriminator.parameters():
            assert parameter.grad is not None


class TestResidual(TestCase):

    def test_forward(self):
        """Test `test_forward` for a generic case.

        Check that the output shapes are correct.
        We can also test that all parameters have a gradient attached to them
        by running `encoder.parameters()`. To do that, we just need to use `loss.backward()`
        for some loss, like `loss = torch.mean(output)`.

        Setup:
            - initialize with input_size, output_size
            - Create random tensor as input

        Input:
            - input = random tensor of shape (N, input_size)

        Output:
            - tensor of shape (N, input_size + output_size)
        """
        residual = Residual(10, 2)
        output = residual(torch.randn(100, 10))
        assert output.shape == (100, 12)

        # Check to make sure no gradients attached
        for parameter in residual.parameters():
            assert parameter.grad is None

        # Backpropagate
        output.mean().backward()

        # Check to make sure all parameters have gradients
        for parameter in residual.parameters():
            assert parameter.grad is not None


class TestGenerator(TestCase):

    def test___init__(self):
        """Test `__init__` for a generic case.

        Make sure 'self.seq' has same length as `generator_dim` + 1.

        Setup:
            - Create Generator

        Input:
            - embedding_dim = positive integer
            - generator_dim = list of integers
            - data_dim = positive integer

        Output:
            - None

        Side Effects:
            - Set `self.seq`
        """
        generator_dim = [1, 2, 3]
        generator = Generator(embedding_dim=50, generator_dim=generator_dim, data_dim=7)

        assert len(generator.seq) == len(generator_dim) + 1

    def test_forward(self):
        """Test `test_forward` for a generic case.

        Check that the output shapes are correct.
        We can also test that all parameters have a gradient attached to them
        by running `encoder.parameters()`. To do that, we just need to use `loss.backward()`
        for some loss, like `loss = torch.mean(output)`.

        Setup:
            - initialize with embedding_dim, generator_dim, data_dim
            - Create random tensor as input

        Input:
            - input = random tensor of shape (N, input_size)

        Output:
            - tensor of shape (N, data_dim)
        """
        generator = Generator(embedding_dim=60, generator_dim=[100, 200, 300], data_dim=500)
        output = generator(torch.randn(70, 60))
        assert output.shape == (70, 500)

        # Check to make sure no gradients attached
        for parameter in generator.parameters():
            assert parameter.grad is None

        # Backpropagate
        output.mean().backward()

        # Check to make sure all parameters have gradients
        for parameter in generator.parameters():
            assert parameter.grad is not None


class TestCTGANSynthesizer(TestCase):

    def test__apply_activate_(self):
        """Test `_apply_activate` for tables with both continuous and categoricals.

        Check every continuous column has all values between -1 and 1
        (since they are normalized), and check every categorical column adds up to 1.

        Setup:
            - Mock `self._transformer.output_info_list`

        Input:
            - data = tensor of shape (N, data_dims)

        Output:
            - tensor = tensor of shape (N, data_dims)
        """

    def test__cond_loss(self):
        """Test `_cond_loss`.

        Test that the loss is purely a function of the target categorical.

        Setup:
            - mock transformer.output_info_list
            - create two categoricals, one continuous
            - compute the conditional loss, conditioned on the 1st categorical
            - compare the loss to the cross-entropy of the 1st categorical, manually computed

        Input:
            data - the synthetic data generated by the model
            c - a tensor with the same shape as the data but with only a specific one-hot vector
                corresponding to the target column filled in
            m - binary mask used to select the categorical column to condition on

        Output:
            loss scalar; this should only be affected by the target column

        Note:
            - this is probably broken right now...
        """

    def test__validate_discrete_columns(self):
        """Test `_validate_discrete_columns` if the discrete column doesn't exist.

        Check the appropriate error is raised if `discrete_columns` is invalid, both
        for numpy arrays and dataframes.

        Setup:
            - Create dataframe with a discrete column
            - Define `discrete_columns` as something not in the dataframe

        Input:
            - train_data = 2-dimensional numpy array or a pandas.DataFrame
            - discrete_columns = list of strings or integers

        Output:
            None

        Side Effects:
            - Raises error if the discrete column is invalid.

        Note:
            - could create another function for numpy array
        """
        data = pd.DataFrame({
            'discrete': ['a', 'b']
        })
        discrete_columns = ['doesnt exist']

        ctgan = CTGANSynthesizer(epochs=1)
        with pytest.raises(ValueError):
            ctgan.fit(data, discrete_columns)

    def test_sample(self):
        """Test `sample` correctly sets `condition_info` and `global_condition_vec`.

        Tests the first 7 lines of sample by mocking the DataTransformer and DataSampler
        and checking that they are being correctly used.

        Setup:
            - Create and fit the synthesizer
            - Mock DataTransformer, DataSampler

        Input:
            - n = integer
            - condition_column = string (not None)
            - condition_value = string (not None)

        Output:
            Not relevant

        Note:
            - I'm not sure we need this test
        """

    def test_set_device(self):
        """Test 'set_device' if a GPU is available.

        Check that decoder/encoder can successfully be moved to the device.
        If the machine doesn't have a GPU, this test shouldn't run.

        Setup:
            - Move decoder/encoder to device

        Input:
            - device = string

        Output:
            None

        Side Effects:
            - Set `self._device` to `device`
            - Moves `self.decoder` to `self._device`

        Note:
            - Need to be careful when checking whether the encoder is actually set
            to the right device, since it's not saved (it's only used in fit).
        """
