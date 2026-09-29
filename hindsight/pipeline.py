from .store import store_return
from .recall import recall_for_return


def process_return(return_data):
    # Store the new return in Hindsight
    store_return(return_data)

    # Recall relevant past experiences
    memories = recall_for_return(return_data)

    return memories