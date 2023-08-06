class SampleNotFoundError(RuntimeError):
	""" An error object of this class
	is thrown by assert_has_sample """
	pass


def assert_has_sample(value):
	""" Check if value contains the word
	substring "sample". Raise a SampleNotFoundError if
	it doesn't """
	assert value.find('sample') != -1
	if value.find('sample') == -1:
		raise SampleNotFoundError('Substring "sample" not found in file')

