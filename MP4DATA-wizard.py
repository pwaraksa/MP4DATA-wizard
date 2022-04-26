import os

# rootdir = 'D:\AndzelikaHaidt_dane_z_gdrive'
print("MP4DATA-wizard - program do eksportu listy plikow mp4, ich lokalizacji na dysku i daty ich utworzenia.")
print("Autor: patryk, p.waraksa@ibles.waw.pl")
print()
print(r"wpisz sciezke folderu (np. D:\folder1\wideo)")

rootdir = str(input())
#'D:\AndzelikaHaidt_dane_z_gdrive'
print(r"powstanie lista z folderu: "+str(rootdir))
print()

def get_mov_timestamps(filename):
    ''' Get the creation and modification date-time from .mov metadata.

        Returns None if a value is not available.
    '''
    from datetime import datetime as DateTime
    import struct

    ATOM_HEADER_SIZE = 8
    # difference between Unix epoch and QuickTime epoch, in seconds
    EPOCH_ADJUSTER = 2082844800

    creation_time = modification_time = None

    # search for moov item
    with open(filename, "rb") as f:
        while True:
            atom_header = f.read(ATOM_HEADER_SIZE)
            # ~ print('atom header:', atom_header)  # debug purposes
            if atom_header[4:8] == b'moov':
                break  # found
            else:
                atom_size = struct.unpack('>I', atom_header[0:4])[0]
                f.seek(atom_size - 8, 1)

        # found 'moov', look for 'mvhd' and timestamps
        atom_header = f.read(ATOM_HEADER_SIZE)
        if atom_header[4:8] == b'cmov':
            raise RuntimeError('moov atom is compressed')
        elif atom_header[4:8] != b'mvhd':
            raise RuntimeError('expected to find "mvhd" header.')
        else:
            f.seek(4, 1)
            creation_time = struct.unpack('>I', f.read(4))[0] - EPOCH_ADJUSTER
            creation_time = DateTime.fromtimestamp(creation_time)
            if creation_time.year < 1990:  # invalid or censored data
                creation_time = None

            modification_time = struct.unpack('>I', f.read(4))[0] - EPOCH_ADJUSTER
            modification_time = DateTime.fromtimestamp(modification_time)
            if modification_time.year < 1990:  # invalid or censored data
                modification_time = None

    return creation_time, modification_time


# %b: Returns the first three characters of the month name. In our example, it returned "Sep"
# %d: Returns day of the month, from 1 to 31. In our example, it returned "15".
# %Y: Returns the year in four-digit format. In our example, it returned "2018".
# %H: Returns the hour. In our example, it returned "00".
# %M: Returns the minute, from 00 to 59. In our example, it returned "00".
# %S: Returns the second, from 00 to 59. In our example, it returned "00".
# %a: Returns the first three characters of the weekday, e.g. Wed.
# %A: Returns the full name of the weekday, e.g. Wednesday.
# %B: Returns the full name of the month, e.g. September.
# %w: Returns the weekday as a number, from 0 to 6, with Sunday being 0.
# %m: Returns the month as a number, from 01 to 12.
# %p: Returns AM/PM for time.
# %y: Returns the year in two-digit format, that is, without the century. For example, "18" instead of "2018".
# %f: Returns microsecond from 000000 to 999999.
# %Z: Returns the timezone.
# %z: Returns UTC offset.
# %j: Returns the number of the day in the year, from 001 to 366.
# %W: Returns the week number of the year, from 00 to 53, with Monday being counted as the first day of the week.
# %U: Returns the week number of the year, from 00 to 53, with Sunday counted as the first day of each week.
# %c: Returns the local date and time version.
# %x: Returns the local version of date.
# %X: Returns the local version of time.

print(r"wpisz sciezke gdzie zapisac liste plikow w formacie txt (np. D:\folder1\zdjecia)")
output_path = str(input())
output_full_path = output_path + r"\lista_plikow_mp4.txt"


with open(output_full_path, "w") as text_file:
    text_file.write("nazwa pliku;full_path;path;data wykonania;czas wykonania\n")
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file[-3:] == "mp4" or file[-3:] == "MP4":
                date_created = get_mov_timestamps(os.path.join(subdir, file))[0]
                date_created_format1 = get_mov_timestamps(os.path.join(subdir, file))[0].strftime("%d-%m-%Y %H:%M:%S")
                date = get_mov_timestamps(os.path.join(subdir, file))[0].strftime("%d.%m.%Y")
                time = get_mov_timestamps(os.path.join(subdir, file))[0].strftime("%H:%M:%S")

                text_file.write(f"{file};{os.path.join(subdir, file)};{os.path.join(subdir)};{date};{time}\n")
                # print(file, os.path.join(subdir, file), os.path.join(subdir), date, time)
print()
print(r"SUKCES!:) lista zapisana w pliku: "+str(output_full_path))
no_input = input()

