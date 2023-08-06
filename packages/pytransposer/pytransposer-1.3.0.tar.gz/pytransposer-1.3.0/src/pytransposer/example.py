from .transposer import transpose_song
from .config import TransposerConfig
TransposerConfig.sharp = 's'
TransposerConfig.flat = '♭'

song = """
Thi\[MI]s is an example \[SI]song
W\[LA]hich is \[MI]going to be transpo\[DOsm]sed\[LA]
"""
# Auto-detect the key of the song from the first chord
transposed_song = transpose_song(song, 1, chord_style_out='doremi')
print(transposed_song)

# Change the symbol for sharps
TransposerConfig.sharp = '#'
song = """
Thi\[MI]s is an example \[SI]song
W\[LA]hich is \[MI]going to be transpo\[DO#m]sed\[LA]
"""
# Transpose to a given key
transposed_song = transpose_song(song, 1, to_key='D#', chord_style_out='abc')
print(transposed_song)

# Change the key half-way through
song = """
Thi\[MI]s is an example \[SI]song\key{DO}
W\[LA]hich is \[MI]going to be transpo\[DO#m]sed\[LA]
"""
# Transpose to a given key
transposed_song = transpose_song(song, 1, to_key='D#', chord_style_out='abc')
print(transposed_song)


TransposerConfig.flat = 'b'

# Change to_key
transposed_song = transpose_song('\nThi\[C]s is \key{SIb}an e\[A]xample \[C]song', 1, to_key='D#', chord_style_out='abc')
print(transposed_song)

transposed_song = transpose_song('Thi\[C]s is \|D##|an e\[A]xample \[C]song', 3, pre_key=r'\\\|', post_key=r'\|')
print(transposed_song)


transposed_song = transpose_song('\|D#|Thi\[C]s is \|-1|an e\[A]xample \[C]song', 3, pre_key=r'\\\|', post_key=r'\|')
print(transposed_song)
