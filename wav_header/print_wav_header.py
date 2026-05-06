import urllib.request

AUDIO_URL = "https://dpgr.am/spacewalk.wav"
# AUDIO_URL = "https://www.mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/Samples/AFsp/M1F1-Alaw-AFsp.wav"
# AUDIO_URL = "https://www.mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/Samples/AFsp/M1F1-int12-AFsp.wav"

def main():
    try:
        print(f"Downloading file '{AUDIO_URL}'...")
        audio_data = urllib.request.urlopen(AUDIO_URL).read()
        print(f"Downloaded {len(audio_data):,} bytes")
        print("Printing HEADER...")
        
        print("\n[Master RIFF chunk]")
        print(f"   FileTypeBlocID  (4 bytes) : '{audio_data[0:4].decode()}'\t\tIdentifier « RIFF »  (0x52, 0x49, 0x46, 0x46)")
        print(f"   FileSize        (4 bytes) : '{int.from_bytes(audio_data[4:8], byteorder='little'):,}'\tOverall file size minus 8 bytes")
        print(f"   FileFormatID    (4 bytes) : '{audio_data[8:12].decode()}'\t\tFormat = « WAVE »  (0x57, 0x41, 0x56, 0x45)")

        print("\n[Chunk describing the data format]")
        print(f"   FormatBlocID    (4 bytes) : '{audio_data[12:16].decode()}'\t\tIdentifier « fmt␣ »  (0x66, 0x6D, 0x74, 0x20)")
        print(f"   BlocSize        (4 bytes) : '{int.from_bytes(audio_data[16:20], byteorder='little'):,}'\t\tChunk size minus 8 bytes, which is 16 bytes here  (0x10)")
        print(f"   AudioFormat     (2 bytes) : '{int.from_bytes(audio_data[20:22], byteorder='little'):,}'\t\tAudio format (1: PCM, 3: IEEE float, 6: 8-bit ITU-T G.711 A-law, 7: 8-bit ITU-T G.711 µ-law)")
        print(f"   NbrChannels     (2 bytes) : '{int.from_bytes(audio_data[22:24], byteorder='little'):,}'\t\tNumber of channels")
        print(f"   Frequency       (4 bytes) : '{int.from_bytes(audio_data[24:28], byteorder='little'):,}'\t\tSample rate (in hertz)")
        print(f"   BytePerSec      (4 bytes) : '{int.from_bytes(audio_data[28:32], byteorder='little'):,}'\t\tNumber of bytes to read per second (Frequency * BytePerBloc)")
        print(f"   BytePerBloc     (2 bytes) : '{int.from_bytes(audio_data[32:34], byteorder='little'):,}'\t\tNumber of bytes per block (NbrChannels * BitsPerSample / 8)")
        print(f"   BitsPerSample   (2 bytes) : '{int.from_bytes(audio_data[34:36], byteorder='little'):,}'\t\tNumber of bits per sample")

        print("\n[Chunk containing the sampled data]")
        print(f"   DataBlocID      (4 bytes) : '{audio_data[36:40].decode()}'\t\tIdentifier « data »  (0x64, 0x61, 0x74, 0x61)")
        print(f"   DataSize        (4 bytes) : '{int.from_bytes(audio_data[40:44], byteorder='little'):,}'\tSampledData size")
        print(f"   SampledData")

    except Exception as e:
        print(f"Excelption: {e}")
        return

if __name__ == "__main__":
    main()
