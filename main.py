import os
import sys

# Import your new working summarizer
from summarizer import summarize_text

# Optional: Import your PDF processor if you want to show off that capability later
# from src import pdf_processor 

def main():
    print("="*60)
    print(" 🚀  DOCACTION: INTELLIGENT SUMMARIZER (OFFLINE AI) ")
    print("="*60)
    print("1. Paste Text (Instant)")
    print("2. Process PDF File (Uses src pipeline)")
    print("="*60)
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        print("\n--- PASTE YOUR TEXT BELOW (Press Enter twice to finish) ---")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        
        raw_text = "\n".join(lines)
        
        if len(raw_text) < 10:
            print("❌ Error: Text too short!")
            return

        print("\n" + "-"*30)
        print("⚡ GENERATING SUMMARY...")
        print("-" * 30)
        
        # CALL THE FUNCTION WE JUST FIXED
        summary = summarize_text(raw_text, percentage=0.3)
        
        print("\n📄 SUMMARY RESULT:")
        print(summary)
        print("\n" + "="*60)

    elif choice == "2":
        # This connects to your 18 files in 'src' when you are ready
        file_path = input("\nEnter PDF file path: ").strip()
        print("Feature coming in next update! (Connecting to src/pipeline.py...)")
        # TODO: Add your PDF logic here later
        
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()