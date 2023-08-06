# %%
import flightplans
print(dir(flightplans))
print(flightplans.__version__)

# %%
from flightplans import flightplans
model = flightplans(verbose=10)
model.fit_transform()

# %%
