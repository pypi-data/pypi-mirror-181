import multiprocessing as mp

import msgpack
import msgpack_numpy as mn
import numpy as np


class ProcessPlotter:
    def __init__(self, output):
        self.output = output

    def terminate(self):
        pass

    def call_back(self):
        import matplotlib.gridspec as gridspec
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_pdf import PdfPages

        self.flag = False

        with PdfPages(f"{self.output}") as pdf:
            while True:
                command = self.pipe.recv()
                if command is None:
                    self.terminate()
                    return False
                else:
                    (
                        section_axio,
                        section_stpt,
                        match_st,
                        dbeads,
                        best_j,
                        im1,
                        array,
                    ) = msgpack.unpackb(
                        command,
                        object_hook=mn.decode,
                        use_list=False,
                        strict_map_key=False,
                    )
                    fig = plt.figure(tight_layout=True, figsize=(8, 12))
                    gs = gridspec.GridSpec(4, 2)

                    ax = fig.add_subplot(gs[0, :])
                    ax.plot(match_st.values())
                    ax.plot([best_j], [match_st[best_j]], "o")
                    ax.set_xlabel("STPT Slice No.")
                    ax.set_ylabel("stat")
                    ax.set_title(f"A: {section_axio} S: {section_stpt}")

                    ax = fig.add_subplot(gs[1, :])
                    vals = sorted(list(dbeads.items()), key=lambda x: x[0])
                    slices = [x[0] for x in vals]
                    nbeads = [x[1] for x in vals]
                    j = np.argmax(nbeads)
                    j = max(j, 5)
                    ax.bar(slices[j - 5 : j + 5], nbeads[j - 5 : j + 5])
                    ax.set_ylabel("beads")

                    ax = fig.add_subplot(gs[2:, :])
                    img = np.zeros((im1.shape[0], im1.shape[1], 3))
                    img[..., 0] = (im1 - im1.min()) / im1.max()
                    img[..., 1] = (array - array.min()) / array.max()

                    ax.imshow(img)
                    ax.axis("off")

                    pdf.savefig()
                    plt.close()
        return True

    def __call__(self, pipe):
        self.pipe = pipe
        self.call_back()


class NBPlot:
    def __init__(self, output):
        self.plot_pipe, plotter_pipe = mp.Pipe()
        self.plotter = ProcessPlotter(output)
        self.plot_process = mp.Process(
            target=self.plotter, args=(plotter_pipe,), daemon=True
        )
        self.plot_process.start()

    def plot(self, *args, finished=False):
        send = self.plot_pipe.send
        if finished:
            send(None)
        else:
            send(args)
