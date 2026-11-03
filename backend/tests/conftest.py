import os

# Before any app import: no GPIO or camera on dev machines / CI.
os.environ["GPIOZERO_PIN_FACTORY"] = "mock"
os.environ["CAMERA_SOURCE"] = "fake"
