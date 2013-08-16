from subprocess import call


def mfold(input):
    """
    Executing mfold to create appropriate files

    """

    with open("mfold_input", "w") as f:
        f.write(input)

    call(["mfold", "seq='mfold_input'"])
