# main.py
import sys
from ppa_agent.agent import PPAA, log_final_status

def main():
    """Main execution loop for the PPAA."""
    print("--- Personal Productivity & Automation Agent (PPAA) Initialized ---")
    try:
        # Initialize the PPAA, which loads the API key and tools
        ppa_agent = PPAA()
    except ValueError as e:
        print(f"ERROR: {e}")
        print("Please ensure your GEMINI_API_KEY is correctly set in the .env file.")
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
            # Run the agent's request processing
            agent_response = ppa_agent.run_request(user_input)
            
            # Log the final completion status of the interaction
            log_final_status(user_input, agent_response)

            print(f"\nPPAA Response: {agent_response}\n")

        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            log_final_status(user_input, "Error")
            print(f"\nERROR: {error_message}\n")

if __name__ == "__main__":
    main()