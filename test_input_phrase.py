class TestInputPhrase:
    def test_input_phrase(self):
        phrase = input("Set a phrase")
        assert len(phrase) < 15, f"The phrase '{phrase}' is longer than 15 characters"
