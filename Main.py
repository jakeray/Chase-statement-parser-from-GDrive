import Parser
import API

continue_program = True

def main():
    while continue_program:
        choice = input("Press 1 for I/O, 2 for Parsing: ")    
        if choice == "1": 
            API.prompt()
        elif choice == "2":
            Parser.Prompt()

if __name__ == "__main__":
    main()