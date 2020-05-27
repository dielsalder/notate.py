import notes
def test_file(filename, export_filename = None):
    segments = notes.get_notes(filename)
    if export_filename:
        segments.export_labels(export_filename)
    print(segments)
test_file('data/twinkle_no_legato.wav')