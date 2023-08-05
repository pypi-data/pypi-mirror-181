import os

def set_headers(datafile, logfile):
    print(os.getcwd())
    labels = {}
    nextfile = None
    nextnote = None

    if os.path.exists(logfile):
        print("exists")
        with open(logfile) as log:
            line = log.readline()
            print(line)
            while line != "":
                while "i: " not in line and line != "":
                    line = log.readline()  # skip the first few lines until you get to viewing geometry
                if "i:" in line:
                    try:
                        nextnote = " (i=" + line.split("i: ")[-1].strip("\n")
                    except:
                        nextnote = " (i=?"
                while "e: " not in line and line != "":
                    line = log.readline()
                if "e:" in line:
                    try:
                        nextnote = nextnote + " e=" + line.split("e: ")[-1].strip("\n")
                    except:
                        nextnote = nextnote + " e=?"
                while "az: " not in line and line != "":
                    line = log.readline()
                if "az:" in line:
                    try:
                        nextnote = nextnote + " az=" + line.split("az: ")[-1].strip("\n") + ")"
                    except:
                        nextnote = nextnote + " az=?)"
                while "filename" not in line and line != "":
                    line = log.readline()
                if "filename" in line:
                    if "\\" in line:
                        line = line.split("\\")
                    else:
                        line = line.split("/")
                    nextfile = line[-1].strip("\n")
                    nextfile = nextfile.split(".")
                    nextfile = nextfile[0] + nextfile[1]

                while "Label" not in line and line != "":
                    line = log.readline()
                if "Label" in line:
                    nextnote = line.split("Label: ")[-1].strip("\n") + nextnote

                if nextfile is not None and nextnote is not None:
                    nextnote = nextnote.strip("\n")
                    labels[nextfile] = nextnote

                    nextfile = None
                    nextnote = None
                line = log.readline()

            data_lines = []
            print(labels)
            if len(labels) != 0:
                with open(datafile, "r") as data:
                    line = data.readline().strip("\n")
                    data_lines.append(line)
                    while line != "":
                        line = data.readline().strip("\n")
                        data_lines.append(line)

                datafiles = data_lines[0].split("\t")[
                            1:
                            ]  # The first header is 'Wavelengths', the rest are file names

                spectrum_labels = []
                unknown_num = (
                    0  # This is the number of files in the datafile headers that aren't listed in the log file.
                )
                for i, filename in enumerate(datafiles):
                    label_found = False
                    filename = filename.replace(".", "")
                    spectrum_label = filename
                    if filename in labels:
                        label_found = True
                        if labels[filename] != "":
                            spectrum_label = labels[filename]

                    # Sometimes the label in the file will have sco attached. Take off the sco
                    # and see if that is in the labels in the file.
                    filename_minus_sco = filename[0:-3]
                    if filename_minus_sco in labels:
                        label_found = True
                        if labels[filename_minus_sco] != "":
                            spectrum_label = labels[filename_minus_sco]

                    if label_found == False:
                        print("Could not find label for spectrum")
                        print(filename)
                        unknown_num += 1
                    spectrum_labels.append(spectrum_label)

                header_line = data_lines[0].split("\t")[0]  # This will just be 'Wavelengths'
                for i, label in enumerate(spectrum_labels):
                    header_line = header_line + "\t" + label

                data_lines[0] = header_line

                with open(datafile, "w") as data:
                    for line in data_lines:
                        data.write(line + "\n")

            # Now reformat data to fit WWU spectral library format.
            data = []
            metadata = [
                "Database of origin:,Western Washington University Planetary Spectroscopy Lab",
                "Sample Name",
                "Viewing Geometry",
            ]

            for i, line in enumerate(data_lines):
                if i == 0:
                    headers = line.split("\t")
                    headers[-1] = headers[-1].strip("\n")
                    for i, header in enumerate(headers):
                        if i == 0:
                            continue
                        # If sample names and geoms were read successfully from logfile, this should always
                        # work fine. But in case logfile is missing or badly formatted, don't break, just don't
                        # have geom info either.
                        try:
                            sample_name = header.split("(")[0]
                        except:
                            sample_name = header
                        try:
                            geom = header.split("(")[1].strip(")")
                        except:
                            geom = ""
                        metadata[1] += "," + sample_name
                        metadata[2] += "," + geom
                    metadata.append("")
                    metadata.append("Wavelength")

                else:
                    data.append(line.replace("\t", ","))

            with open(datafile, "w+") as file:
                for line in metadata:
                    file.write(line)
                    file.write("\n")
                for line in data:
                    file.write(line)
                    file.write("\n")

            if len(labels) == 0:
                return "nolabels"
            elif unknown_num == 0:
                return ""  # No warnings
            elif unknown_num == 1:
                return "1unknown"  # This will succeed but the control computer will print a warning that not all
                # samples were labeled. Knowing if it was one or more than one just helps with grammar.

            elif unknown_num > 1:
                return "unknowns"
    else:
        return "nolog"

set_headers("newfile.txt", "C:\\Users\kathleen\PythonProjects\\tanager-feeder\\asd_feeder\\scratch_log.txt")