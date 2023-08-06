import matplotlib.pyplot as plt
import io


def GetPlotImageData():
    byte_form = io.BytesIO()
    plt.savefig(byte_form)
    plt.close()

    return byte_form
