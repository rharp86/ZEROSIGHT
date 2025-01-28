import sys
import re

def get_targets():
    print("Enter target(s) (IP, CIDR, or domain), separated by commas: ", end="", flush=True)

    try:
        # Set a timeout to prevent indefinite blocking
        import select
        ready, _, _ = select.select([sys.stdin], [], [], 10)  # Timeout after 10 seconds
        if not ready:
            print("\nNo input detected. Exiting.")
            sys.exit(1)

        # Read input and clean up unwanted characters
        target_input = sys.stdin.readline().strip()
        target_input = re.sub(r'[\r\n\x00-\x1F\x7F]', '', target_input)

        # Split targets by commas and return a list
        targets = [t.strip() for t in target_input.split(",") if t.strip()]
        return targets
    except KeyboardInterrupt:
        print("\nInput interrupted by user. Exiting.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input: {str(e)}")
        sys.exit(1)
