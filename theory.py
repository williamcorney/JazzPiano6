# theory.py
def get_theory(tab1_instance):
    # Set the required_notes to [60, 62, 64]
    tab1_instance.theorymode = "Scales"
    if tab1_instance.theorymode == "Scales":
        tab1_instance.required_notes = [60, 62, 64]
        print (tab1_instance.theorymode)
        print(f"Required notes set to: {tab1_instance.required_notes}")
