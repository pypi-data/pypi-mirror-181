from ipykernel.kernelapp import IPKernelApp
from . import DummyKernel

IPKernelApp.launch_instance(kernel_class=DummyKernel)
