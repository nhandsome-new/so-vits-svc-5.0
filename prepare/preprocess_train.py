import os
import random


def print_error(info):
    print(f"\033[31m File isn't existed: {info}\033[0m")


if __name__ == "__main__":
    os.makedirs("./files/", exist_ok=True)

    rootPaths = [
        "/data/fusic/", "/data/hq_eng_song","/data/karanovc_min",
        "/data/song_22k/song_CSD_en_kr","/data/song_22k/song_MedleyVox_en",
        "/data/youtube_selected"
    ]
    all_items = []
    for rootPath in rootPaths:
        for spks in os.listdir(f"{rootPath}"):
        # for spks in [f"jvs{i+1:0>3}" for i in range(10)]:
            if not os.path.isdir(f"{rootPath}/{spks}"):
                continue
            
            file_list = os.listdir(f"{rootPath}/{spks}/wav")  
                
            for file in file_list:
                if file.endswith(".wav"):
                    file = file[:-4]
                    path_spk = f"{rootPath}/{spks}/spkemb/{file}.g.pt"    # [512]
                    path_wave = f"{rootPath}/{spks}/wav/{file}.wav"     # [1,T]     T=200670
                    path_spec = f"{rootPath}/{spks}/spec/{file}.pt"     # [513,T]   T=783
                    path_pitch = f"{rootPath}/{spks}/f0uv/{file}.f0.npy"   #[T]     T=783
                    path_hubert = f"{rootPath}/{spks}/content/{file}.c.pt"    # [T, 256]  T=455
                    path_whisper = f"{rootPath}/{spks}/{file}.ppg.npy"
                    has_error = 0
                    if not os.path.isfile(path_spk):
                        print_error(path_spk)
                        has_error = 1
                    if not os.path.isfile(path_wave):
                        print_error(path_wave)
                        has_error = 1
                    if not os.path.isfile(path_spec):
                        print_error(path_spec)
                        has_error = 1
                    if not os.path.isfile(path_pitch):
                        print_error(path_pitch)
                        has_error = 1
                    if not os.path.isfile(path_hubert):
                        print_error(path_hubert)
                        has_error = 1
                    # if not os.path.isfile(path_whisper):
                    #     print_error(path_whisper)
                    #     has_error = 1
                    if has_error == 0:
                        all_items.append(
                            f"{path_wave}|{path_spec}|{path_pitch}|{path_hubert}|{path_whisper}|{path_spk}")

    random.shuffle(all_items)
    valids = all_items[:10]
    valids.sort()
    trains = all_items[10:]
    # trains.sort()
    fw = open("./files/valid_big_with_song.txt", "w", encoding="utf-8")
    for strs in valids:
        print(strs, file=fw)
    fw.close()
    fw = open("./files/train_big_with_song.txt", "w", encoding="utf-8")
    for strs in trains:
        print(strs, file=fw)
    fw.close()
