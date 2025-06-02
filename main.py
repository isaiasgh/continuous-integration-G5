"""Gym membership system for managing membership plans and calculating costs with discounts."""

MEMBERSHIP_PLANS = {
    "basic": 100,
    "premium": 180,
    "family": 250
}

ADDITIONAL_FEATURES = {
    "personal_training": 50,
    "group_classes": 30,
    "spa_access": 40,
    "vip_facilities": 60
}

DISCOUNT_THRESHOLDS = {
    "group": 0.90,  # 10% discount
    "high_value": 400,  # $50 discount threshold
    "medium_value": 200,  # $20 discount threshold
    "premium_surcharge": 1.15  # 15% surcharge
}

def main():
    """Main function that runs the gym membership system program."""
    print("Welcome to the gym membership system")
    while True:
        try:
            membership = select_membership()
            extras = select_additional_features()
            group_size = get_group_size()
            total, results = calculate_total_cost(membership, extras, group_size)
            confirm = confirm_selection(membership, extras, total, results)

            if confirm:
                print(f"\nFinal total cost: ${int(total)}")
                break
            print("\nProcess cancelled. Starting over...\n")
        except ValueError as e:
            print(f"Error: {e}\n")
        except TypeError as e:
            print(f"Error: Invalid type - {e}\n")
        except KeyboardInterrupt:
            print("\nProgram terminated by user.")
            break

def select_membership():
    """Prompts user to select a membership plan and returns the selection."""
    print("\nAvailable plans:")
    for plan, cost in MEMBERSHIP_PLANS.items():
        print(f"- {plan.capitalize()} (${cost})")

    choice = input("\nChoose a membership plan: ").strip().lower()
    if choice not in MEMBERSHIP_PLANS:
        raise ValueError("Membership plan not available.")
    return {"type": choice, "cost": MEMBERSHIP_PLANS[choice]}

def select_additional_features():
    """Allows user to select additional features for their membership."""
    selected = []
    print("\nAvailable additional features:")
    for feature, cost in ADDITIONAL_FEATURES.items():
        print(f"- {feature.replace('_', ' ').capitalize()} (${cost})")

    while True:
        choice = input("\nEnter a feature name to add (or 'done'): ").strip().lower()
        if choice == 'done':
            break
        key = choice.replace(' ', '_')
        if key in ADDITIONAL_FEATURES:
            selected.append({"feature": key, "cost": ADDITIONAL_FEATURES[key]})
        else:
            print("Feature not available. Please try again.")

    return selected

def get_group_size():
    """Prompts user for group size and returns the number of people signing up together."""
    try:
        size = int(input("""\n
                          How many people will sign up together? \n 
                          **10% DISCOUNT FOR 2 OR MORE PEOPLE**: 
                          """))
        if size < 1:
            raise ValueError("Must be at least one person.")
        return size
    except ValueError as exc:
        raise ValueError("Invalid input for group size.") from exc
    
def calculate_total_cost(membership, features, group_size):
    """
    Calculates the total cost including membership, features, and applicable discounts/surcharges.
    """
    base_cost = membership['cost']
    extras_cost = sum(f['cost'] for f in features)
    total = base_cost + extras_cost
    results = []

    if group_size >= 2:
        total *= DISCOUNT_THRESHOLDS["group"]
        print("Group discount applied (10%)")
        results.append("Group discount applied (10%)")

    if total > DISCOUNT_THRESHOLDS["high_value"]:
        total -= 50
        print("Special discount applied: $50")
        results.append("Special discount applied: $50")
        
    elif total > DISCOUNT_THRESHOLDS["medium_value"]:
        total -= 20
        print("Special discount applied: $20")
        results.append("Special discount applied: $20")

    if membership['type'] == 'premium' or any(f['feature'] == 'vip_facilities' for f in features):
        total *= DISCOUNT_THRESHOLDS["premium_surcharge"]
        print("Premium membership surcharge applied (15%)")
        results.append("Premium membership surcharge applied (15%)")

    return total, results

def confirm_selection(membership, features, total, results):
    """Displays selection summary and prompts user for confirmation."""
    print("\nSelection summary:")
    print(f"- Plan: {membership['type'].capitalize()} (${membership['cost']})")
    print("- Additional features:")
    for f in features:
        print(f"  * {f['feature'].replace('_', ' ').capitalize()} (${f['cost']})")
    for result in results:
        print(f"- {result}")
    print(f"- Calculated total: ${int(total)}")
    choice = input("\nDo you confirm this selection? (y/n): ").strip().lower()
    return choice == 'y'

if __name__ == "__main__":
    main()
