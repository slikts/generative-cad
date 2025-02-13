# https://github.com/CadQuery/cadquery/issues/874#issuecomment-2257759146

from math import cos, pi, radians, sin, tan

from cadquery import Face, Shell, Solid, Workplane


class Thread(object):
    """a base class to represents threads of all kinds"""

    def __init__(self, nominal, passdrill, threaddrill, pitch):
        self.nominal = nominal
        self.pitch = pitch
        self.passdrill = passdrill
        self.threaddrill = threaddrill


class ISOThread(Thread):
    """the parameters in ISO threads"""

    def __init__(self, nominal, passdrill, threaddrill, pitch):
        super(ISOThread, self).__init__(nominal, passdrill, threaddrill, pitch)
        # derived
        self.veeheight = pitch / (2 * tan(radians(30)))
        self.Dmajor = nominal
        self.Dminor = nominal - 2 * self.veeheight * 5 / 8


class UTSThread(ISOThread):
    """IMO UTS thread has the same defintions as ISO thread,
    so we can simply delegate (for now ?)
    """

    def __init__(self, nominal, passdrill, threaddrill, pitch):
        super(UTSThread, self).__init__(nominal, passdrill, threaddrill, pitch)


threads = {
    "M1.5": ISOThread(1.5, 1.60, 1.15, 0.35),
    "M1.6": ISOThread(1.6, 1.70, 1.25, 0.35),
    "M1.8": ISOThread(1.8, 1.90, 1.45, 0.35),
    "M2": ISOThread(2.0, 2.10, 1.60, 0.40),
    "M2.5": ISOThread(2.5, 2.65, 2.05, 0.45),
    "M3": ISOThread(3.0, 3.15, 2.50, 0.50),
    "M4": ISOThread(4.0, 4.20, 3.30, 0.70),
    "M5": ISOThread(5.0, 5.25, 4.20, 0.80),
    "M5 0.5": ISOThread(5.0, 5.25, 4.50, 0.50),
    "M5.5 0.5": ISOThread(5.5, 5.75, 5.00, 0.50),
    "M6": ISOThread(6.0, 6.30, 5.00, 1.00),
    "M8": ISOThread(8.0, 8.40, 6.80, 1.25),
    "M10": ISOThread(10.0, 10.50, 8.50, 1.50),
    "M12": ISOThread(12.0, 12.50, 10.2, 1.75),
    "M16": ISOThread(16.0, 16.9, 14.0, 2.0),
    "M16 1.5": ISOThread(16.0, 16.9, 14.6, 1.50),
    "M20": ISOThread(20.0, 21.0, 17.5, 2.5),
    "M20 1.5": ISOThread(20.0, 21.0, 18.5, 1.50),
    "M24": ISOThread(24.0, 25.0, 21.0, 3.0),
    "Size 2 56": UTSThread(0.0860 * 25.4, 0.0890 * 25.4, 0.0700 * 25.4, 25.4 / 56),
    "Size 2 64": UTSThread(0.0860 * 25.4, 0.0890 * 25.4, 0.0700 * 25.4, 25.4 / 64),
    "1/4 20": UTSThread(0.2500 * 25.4, 0.2570 * 25.4, 0.2010 * 25.4, 25.4 / 20),
    "3/8 16": UTSThread(0.3750 * 25.4, 0.3870 * 25.4, 0.3160 * 25.4, 25.4 / 16),
    "5/8 11": UTSThread(5 * 25.4 / 8, 37 * 25.4 / 64, 17 * 25.4 / 32, 25.4 / 11),
    "1 32": UTSThread(1.0000 * 25.4, 1.0 * 25.4 + 0.4, 0.9617 * 25.4, 25.4 / 32),
    "30mm 32tpi": UTSThread(30.0, 30.4, 29.208, 25.4 / 32),
}


def thread(size, length, location="external", SEGMENTS=60):
    """
    size: the thread we want to generate, e.g.: 'M12'
        or a 'special' thread subclassed from ISOThread and siblings
    length: length in mm
    location: either 'internal' or 'external'
    SEGMENTS: [default: 60] number of segments to divide the circular paths
            less runs faster
            more may produce smoother results (not certain)
    """

    # a local helper routine
    # as we define it inside the main function it will not be visible to the external world
    def helix(r0, cut, pitch, height, d=0):  # , frac=0.185):
        """
        returns the function to compute the (x, y, z) sets to describe the helix
        forming the thread

        r0:     either Dmajor (internal) or Dminor (external)
        cut:    the depth of the thread
        pitch:  the pitch of the thread
        height: the desired length of the thread
        d:      is the offset of the generated helix in regard with the middle of the thread
        """

        # frac:  defines the start and end sections of the thread which starts from a zero profile
        #        up to the full thread profile and ends on a zero profile
        #        a greater value extends the build-up while a smaller shortens it and more specifically
        #        will make the thread extend below and above the specified length
        #        ideally `frac` should be derived from the pitch and the length?
        #        the 0.685 value is empirically determined ovet the current set of defined threads
        frac = 0.685 * pitch / height

        def func(t):
            if t <= frac:
                # thread start
                z = height * t + d * sin(pi / 2 * t / frac)
                r = r0 + cut * sin(pi / 2 * t / frac)
            elif t >= 1 - frac:
                # thread ending
                z = height * t - d * sin(2 * pi - pi / 2 * (1 - t) / frac)
                r = r0 - cut * sin(2 * pi - pi / 2 * (1 - t) / frac)
            else:
                # thread middle
                z = height * t + d
                r = r0 + cut

            x = r * sin(-2 * pi / (pitch / height) * t)
            y = r * cos(2 * pi / (pitch / height) * t)

            return x, y, z

        return func

    if isinstance(size, str):
        th = threads[size]
    elif isinstance((ISOThread, UTSThread)):
        th = size
    else:
        raise ValueError(f" Unknown thread {size} specified!")

    pitch = th.pitch
    veeheight = th.veeheight
    # `epsilon` will add clearance for the thread
    # and at the same time ensure that the thread 'merges' well with the wall it will attached to
    # the 10 was emprically determined, so there definitely may be some optimization here
    # a fixed value for all may generate an 'invisible' thread (which of cours won't be there ...)
    epsilon = threads[size].pitch / 10
    if epsilon < 0.025:
        # enforce a minimum 0.1mm fit margin
        epsilon = 0.025

    if isinstance(th, (ISOThread, UTSThread)):
        if location.startswith("ext"):
            radius = th.Dminor / 2 - epsilon
            h1 = (pitch * 3 / 4) / 2
            h2 = (pitch / 8) / 2
            cut = veeheight * 5 / 8
        else:
            radius = th.Dmajor / 2 + epsilon
            h1 = (pitch * 7 / 8) / 2
            h2 = (pitch / 4) / 2
            cut = -veeheight * 5 / 8
    else:
        raise ValueError('Currently only "ISO and UTS threads" are implemented')

    if DEBUG:
        print(
            f"    {pitch=}, {location=}, {radius=}, {epsilon=},\n    {veeheight=}, {h1=}, {h2=}, {cut=}"
        )

    N = int((length / pitch) * SEGMENTS)

    e1_bot = (
        Workplane("XY")
        .parametricCurve(helix(radius, 0, pitch, length, d=-h1), N=N, smoothing=None)
        .val()
    )
    e1_top = (
        Workplane("XY")
        .parametricCurve(helix(radius, 0, pitch, length, d=h1), N=N, smoothing=None)
        .val()
    )
    e2_bot = (
        Workplane("XY")
        .parametricCurve(helix(radius, cut, pitch, length, d=-h2), N=N, smoothing=None)
        .val()
    )
    e2_top = (
        Workplane("XY")
        .parametricCurve(helix(radius, cut, pitch, length, d=h2), N=N, smoothing=None)
        .val()
    )

    f1 = Face.makeRuledSurface(e1_bot, e1_top)
    f2 = Face.makeRuledSurface(e2_bot, e2_top)
    f3 = Face.makeRuledSurface(e1_bot, e2_bot)
    f4 = Face.makeRuledSurface(e1_top, e2_top)

    sh = Shell.makeShell([f1, f2, f3, f4])
    rv = Solid.makeSolid(sh)

    return rv if location.startswith("int") else rv.rotate([0, 0, 0], [0, 0, 1], 180)


def nthread(size, location="external", threadonly=True):
    """a simple wrapper to allow adding 'flesh' to the thread"""

    NBR_OF_TURNS = 6
    length = threads[size].pitch * NBR_OF_TURNS

    if location.lower().startswith("ext"):
        base = Workplane("XY")
        if not threadonly:
            bodyradius = threads[size].Dminor / 2
            if DEBUG:
                print(f"    {bodyradius=}")
            base = base.circle(bodyradius).extrude(length)
        base += thread(size, length, location="external")
    else:
        base = Workplane("XY")
        if not threadonly:
            holeradius = threads[size].Dmajor / 2
            if DEBUG:
                print(f"    {holeradius=}")
            base = (
                base.rect(holeradius * 2.5, holeradius * 2.5)
                .circle(holeradius)
                .extrude(length)
            )
        base += thread(size, length, location="internal")

    return base


DEBUG = False
if DEBUG:
    import os
    import time

    def writestep(model, *args, **kwargs):
        t = model(*args, **kwargs)
        # assert there is a step subdirectory
        if not os.path.exists("step"):
            # create it
            os.mkdir("step")
        # append all args and kwargs ...#
        fs = [f"{model.__name__}"]
        for arg in args:
            fs.append(f"{arg}")
        for kwarg in kwargs:
            fs.append(f"{kwarg}")
        fname = "_".join(fs)
        fname = fname.replace("/", "o")
        t.val().exportStep(f"step/{fname}.step")

    # exercise all threads, internal and external
    now = time.monotonic_ns()
    for location in ["internal", "external"]:
        print(f"{location=}")
        for size in threads.keys():
            print(f"  {size}")
            writestep(nthread, size, location)
    spent = (time.monotonic_ns() - now) / 1e9
    print(f"Done in {spent} seconds!")

else:
    # to show in CQ-editor, set `Autoreload` active and it will follow the changes
    nthreadt = nthread("5/8 11", "External")
