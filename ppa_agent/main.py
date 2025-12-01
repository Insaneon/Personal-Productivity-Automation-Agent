import sys
from agent import PPAA, log_final_status

def main():
    print("--- Personal Productivity & Automation Agent (PPAA) Initialized ---")
    try:
        ppa_agent = PPAA()
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    
    print(f"Model: {ppa_agent.agent.model}")
    print("Enter 'quit' or 'exit' to end the session.")
    print("------------------------------------------------------------------\n")

    while True:
        user_input = input("User Request: ")
        
        if user_input.lower() in ['quit', 'exit']:
            print("\nPPAA session ended. Goodbye!")
            break
        
        if not user_input.strip():
            continue

        try:
            agent_response = ppa_agent.run_request(user_input)
            
            log_final_status(user_input, agent_response)

            print(f"\nPPAA Response: {agent_response}\n")

        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            log_final_status(user_input, "Error")
            print(f"\nERROR: {error_message}\n")

if __name__ == "__main__":
    main()