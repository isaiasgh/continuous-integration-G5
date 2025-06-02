"""Gym membership system for managing membership plans and calculating costs with discounts."""
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
            else:
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
    memberships = {
        "basic": 100,
        "premium": 180,
        "family": 250
    }
    print("\nAvailable plans:")
    for k, v in memberships.items():
        print(f"- {k.capitalize()} (${v})")

    choice = input("\nChoose a membership plan: ").strip().lower()
    if choice not in memberships:
        raise ValueError("Membership plan not available.")
    return {"type": choice, "cost": memberships[choice]}

def select_additional_features():
    """Allows user to select additional features for their membership."""
    available_features = {
        "personal_training": 50,
        "group_classes": 30,
        "spa_access": 40,
        "vip_facilities": 60  # Premium
    }

    selected = []
    print("\nAvailable additional features:")
    for f, c in available_features.items():
        print(f"- {f.replace('_', ' ').capitalize()} (${c})")

    while True:
        choice = input("\nEnter a feature name to add (or 'done'): ").strip().lower()
        if choice == 'done':
            break
        key = choice.replace(' ', '_')
        if key in available_features:
            selected.append({"feature": key, "cost": available_features[key]})
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
        total *= 0.90  # 10% discount
        print("Group discount applied (10%)")
        results.append("Group discount applied (10%)")

    if total > 400:
        total -= 50
        print("Special discount applied: $50")
        results.append("Special discount applied: $50")

    elif total > 200:
        total -= 20
        print("Special discount applied: $20")
        results.append("Special discount applied: $20")

    if membership['type'] == 'premium' or any(f['feature'] == 'vip_facilities' for f in features):
        total *= 1.15  # 15% surcharge
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
