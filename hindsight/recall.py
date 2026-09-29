from .memory import client, BANK_ID


def recall_memories(query):
    result = client.recall(
        bank_id=BANK_ID,
        query=query
    )

    return result.results


def classify_memory(memory):
    text = memory.text.lower()

    outcome_keywords = [
        "returnsense outcome",
        "recommended action:",
        "action taken:",
        "outcome:",
        "recommendation:",
        "clearer product dimensions",
        "size guidance were added",
        "size guidance was added",
        "product information was updated",
        "previous recommendation",
    ]

    for keyword in outcome_keywords:
        if keyword in text:
            return "OUTCOME"

    return "RETURN"


def extract_order_id(memory):
    """
    Extract an explicit Order ID from a Hindsight memory.
    """

    for line in memory.text.splitlines():
        line = line.strip()

        if line.startswith("Order ID:"):
            return line.split(":", 1)[1].strip()

    return None


def memory_mentions_current_return(memory, return_data):
    """
    Detect summary memories that describe the current return
    even when they do not contain an explicit Order ID.
    """

    text = memory.text.lower()

    customer_id = str(return_data["customer_id"]).lower()
    product_id = str(return_data["product_id"]).lower()
    current_order_id = str(return_data["order_id"]).lower()
    reason = str(return_data["return_reason"]).lower()

    # If the current Order ID is explicitly mentioned,
    # this memory belongs to the current return.
    if current_order_id in text:
        return True

    # Detect common summary wording describing the current
    # customer + product + reason combination.
    current_customer_product = (
        customer_id in text
        and product_id in text
    )

    current_reason = reason in text

    summary_words = [
        "pattern",
        "returned",
        "returning",
        "return history",
        "return experience",
        "multiple return",
        "repeated",
    ]

    describes_return = any(
        word in text for word in summary_words
    )

    if (
        current_customer_product
        and current_reason
        and describes_return
    ):
        return True

    return False


def deduplicate_return_memories(memories):
    """
    Multiple Hindsight memory units can describe the same
    real-world return.

    Keep only one memory for each distinct Order ID.
    """

    unique_memories = []
    seen_order_ids = set()

    for memory in memories:

        order_id = extract_order_id(memory)

        if order_id:

            if order_id in seen_order_ids:
                continue

            seen_order_ids.add(order_id)

        unique_memories.append(memory)

    return unique_memories


def remove_current_return(memories, return_data):
    """
    Remove memories belonging to the current return.

    This prevents the current return from being treated
    as historical evidence.
    """

    filtered_memories = []

    for memory in memories:

        # First remove memories with the current Order ID.
        order_id = extract_order_id(memory)

        if order_id == str(return_data["order_id"]):
            continue

        # Then remove summary memories that clearly describe
        # the current customer/product/reason combination.
        if memory_mentions_current_return(
            memory,
            return_data
        ):
            continue

        filtered_memories.append(memory)

    return filtered_memories


def recall_for_return(return_data):

    query = f"""
    Find relevant PAST return experiences and previous
    ReturnSense outcomes for this new return.

    IMPORTANT:
    The current return must NOT be treated as a past return.

    Current Order ID: {return_data['order_id']}
    Customer ID: {return_data['customer_id']}
    Product ID: {return_data['product_id']}
    Product Category: {return_data['category']}
    Return Reason: {return_data['return_reason']}

    Look for:
    - previous returns by the same customer
    - previous returns of the same product
    - returns of the same product by other customers
    - similar return reasons
    - recurring category patterns
    - previous ReturnSense recommendations
    - previous actions and outcomes
    """

    memories = recall_memories(query)

    return_memories = []
    outcome_memories = []

    for memory in memories:

        memory_type = classify_memory(memory)

        if memory_type == "OUTCOME":
            outcome_memories.append(memory)

        else:
            return_memories.append(memory)

    # Remove duplicate memory units.
    return_memories = deduplicate_return_memories(
        return_memories
    )

    # Remove the current return and summaries describing it.
    return_memories = remove_current_return(
        return_memories,
        return_data
    )

    return {
        "return_memories": return_memories,
        "outcome_memories": outcome_memories
    }