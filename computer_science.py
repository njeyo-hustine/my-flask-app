# ================================================================
# EDUTEXT COMPUTER SCIENCE QUESTION BANK
# ================================================================


def get_computer_science():
    return {
        "name": "Computer Science",

        "questions": [

            # --- EXAM SHEET QUESTIONS (1 to 17) ---

            {
                "id": 1,
                "question_text": (
                    "Peter authorizes John to withdraw money from his account "
                    "as he was sick. However, he could not withdraw the money "
                    "because of a denial of service attack. Which security "
                    "measure was not attended to?"
                ),
                "options": {
                    "A": "Privacy",
                    "B": "Integrity",
                    "C": "Availability",
                    "D": "Confidentiality"
                },
                "answer": "C",
                "explanation": (
                    "A Denial of Service (DoS) attack directly impacts "
                    "Availability by preventing authorized users from accessing "
                    "services or resources."
                ),
                "hint": "Think about whether the service was accessible when needed."
            },

            {
                "id": 2,
                "question_text": (
                    "Data Compression Techniques are particularly used for; EXCEPT"
                ),
                "options": {
                    "A": "reductions in storage hardware",
                    "B": "data transmission time",
                    "C": "communication bandwidth",
                    "D": "effect of errors in transmission"
                },
                "answer": "D",
                "explanation": (
                    "Data compression reduces file size to save storage space "
                    "and transmission time/bandwidth, but it does not address "
                    "or correct transmission errors."
                ),
                "hint": "Identify which option relates to error handling rather than sizing."
            },

            {
                "id": 3,
                "question_text": (
                    "What is the hexadecimal conversion of the decimal number 224?"
                ),
                "options": {
                    "A": "1E",
                    "B": "0E",
                    "C": "E0",
                    "D": "E1"
                },
                "answer": "C",
                "explanation": (
                    "224 / 16 = 14 remainder 0. "
                    "In hexadecimal, 14 is represented as E, giving E0."
                ),
                "hint": "224 divided by 16 leaves no remainder, and 14 in hex is E."
            },

            {
                "id": 4,
                "question_text": "Give the boolean expression for the circuit:",
                "options": {
                    "A": r"\overline{(A \cdot B)} \cdot \overline{(A + C)}",
                    "B": r"\overline{(A + B)} \cdot \overline{(A + C)}",
                    "C": r"\overline{(A + B)} \cdot \overline{(A \cdot C)}",
                    "D": r"\overline{(A \cdot B)} \cdot \overline{(A \cdot C)}"
                },
                "answer": "B",
                "explanation": (
                    "The circuit consists of a NOR gate for inputs A and B, "
                    "and another NOR gate for inputs A and C, fed into an AND gate."
                ),
                "hint": "Trace the logic gates from inputs A, B, and C to the final output."
            },

            {
                "id": 5,
                "question_text": (
                    "Which of the following corresponds to this assertion:- "
                    "Ngu (A) eats beans or (B) eats rice, and does exactly one "
                    "of the following: (C) drinks wine or (D) eats fruits."
                ),
                "options": {
                    "A": r"(A \otimes B) \cdot (C + D)",
                    "B": r"(A \cdot B) \cdot (C \otimes D)",
                    "C": r"(A + B) \cdot \overline{(C + D)}",
                    "D": r"(A + B) \cdot (C \otimes D)"
                },
                "answer": "D",
                "explanation": (
                    "'Eats beans OR eats rice' represents inclusive OR (A + B). "
                    "'Does exactly one of...' represents Exclusive OR (XOR, represented by ⊗)."
                ),
                "hint": "'Exactly one' maps to the XOR (⊗) operation."
            },

            {
                "id": 6,
                "question_text": "How many inputs and output does a half adder have?",
                "options": {
                    "A": "Two inputs and two outputs",
                    "B": "Two inputs one output",
                    "C": "Three inputs, two outputs",
                    "D": "Three outputs, two inputs"
                },
                "answer": "A",
                "explanation": (
                    "A half adder accepts two inputs (A, B) and produces "
                    "two outputs (Sum and Carry)."
                ),
                "hint": "A half adder produces both a Sum and a Carry."
            },

            {
                "id": 7,
                "question_text": (
                    "If A, B and C_in are the inputs of a full adder, then the sum "
                    "is given by:"
                ),
                "options": {
                    "A": "A AND B XOR C",
                    "B": "A OR B AND C",
                    "C": "A XOR B XOR C",
                    "D": "A EX-NOR B AND C"
                },
                "answer": "C",
                "explanation": (
                    "The Sum logic of a full adder is computed by taking the "
                    "XOR of all three inputs: Sum = A ⊕ B ⊕ C_in."
                ),
                "hint": "Sum in binary addition relies on the XOR operation across inputs."
            },

            {
                "id": 8,
                "question_text": (
                    "These are software which could be gotten and distributed to others."
                ),
                "options": {
                    "A": "Freeware",
                    "B": "Share Ware",
                    "C": "Public domain software",
                    "D": "Free software"
                },
                "answer": "C",
                "explanation": (
                    "Public domain software carries no copyright restrictions, "
                    "allowing anyone to modify, use, and distribute it freely."
                ),
                "hint": "Look for the category that has no copyright restrictions."
            },

            {
                "id": 9,
                "question_text": (
                    "Transmissions in computer data communication is focused on:"
                ),
                "options": {
                    "A": "secure connections to destination",
                    "B": "least complex transmission of data",
                    "C": "safe transmission of data to destination",
                    "D": "adhering to network protocols"
                },
                "answer": "C",
                "explanation": (
                    "The core objective of data communication systems is the "
                    "safe and reliable delivery of data from source to destination."
                ),
                "hint": "Focus on the primary goal of transmitting data accurately."
            },

            {
                "id": 10,
                "question_text": (
                    "Nsh wants all its branch offices in each city to be connected "
                    "before connecting to the head office. Their connectivity is "
                    "best using a:"
                ),
                "options": {
                    "A": "wide area network",
                    "B": "local area network",
                    "C": "virtual private network",
                    "D": "metropolitan area network"
                },
                "answer": "D",
                "explanation": (
                    "A Metropolitan Area Network (MAN) spans a city or town, "
                    "making it ideal for interconnecting branch offices across a city."
                ),
                "hint": "Which network type covers a geographic area the size of a city?"
            },

            {
                "id": 11,
                "question_text": (
                    "It mediates network use well, but becomes useless given a "
                    "single point failure. It has a:"
                ),
                "options": {
                    "A": "bus topology",
                    "B": "star topology",
                    "C": "mesh topology",
                    "D": "network topology"
                },
                "answer": "B",
                "explanation": (
                    "In a star topology, all devices connect to a central hub/switch. "
                    "If the central device fails, the entire network fails."
                ),
                "hint": "Think about a topology controlled by a single central node."
            },

            {
                "id": 12,
                "question_text": (
                    "When you start up a computer and happen to restart it "
                    "because of a freeze or installation, it is called:"
                ),
                "options": {
                    "A": "restore boot",
                    "B": "warm boot",
                    "C": "cold boot",
                    "D": "short boot"
                },
                "answer": "B",
                "explanation": (
                    "Restarting a computer that is already powered on without "
                    "turning off the main power supply is known as a warm boot."
                ),
                "hint": "Restarting while power is already on is 'warm'."
            },

            {
                "id": 13,
                "question_text": (
                    "A malware program that replicates itself and spread without "
                    "any trigger from a user is called a:"
                ),
                "options": {
                    "A": "trojan horse",
                    "B": "spyware",
                    "C": "virus",
                    "D": "worm"
                },
                "answer": "D",
                "explanation": (
                    "A computer worm can self-replicate and spread independently "
                    "across networks without needing user intervention."
                ),
                "hint": "Unlike viruses, this malware spreads completely on its own."
            },

            {
                "id": 14,
                "question_text": (
                    "Which of the unsigned numbers listed below is the largest?"
                ),
                "options": {
                    "A": "101101001_2",
                    "B": "30A_16",
                    "C": "356_10",
                    "D": "11010011_2"
                },
                "answer": "B",
                "explanation": (
                    "Converting all to decimal:\n"
                    "101101001₂ = 361\n"
                    "30A₁₆ = 778\n"
                    "356₁₀ = 356\n"
                    "11010011₂ = 211\n"
                    "Therefore, 30A₁₆ (778) is the largest."
                ),
                "hint": "Convert all numbers to decimal base 10 to compare."
            },

            {
                "id": 15,
                "question_text": (
                    "The process of transferring data to and from backing store "
                    "to immediate state so that other programs can run is known as:"
                ),
                "options": {
                    "A": "Scheduling",
                    "B": "Virtualization",
                    "C": "Caching",
                    "D": "Swapping"
                },
                "answer": "D",
                "explanation": (
                    "Swapping is the memory management mechanism where process data "
                    "is moved between main memory and secondary storage."
                ),
                "hint": "Moving memory blocks back and forth to secondary storage."
            },

            {
                "id": 16,
                "question_text": (
                    "An address bus from a storage unit has 20 bus lines. What is "
                    "the capacity of the storage unit? (Assume 1GB = 1024MB and "
                    "1MB = 1024Kb)"
                ),
                "options": {
                    "A": "2 Mb",
                    "B": "2 Kb",
                    "C": "1 Mb",
                    "D": "1Kb"
                },
                "answer": "C",
                "explanation": (
                    "20 address lines provide 2^20 addressable locations, "
                    "which corresponds to 1 Megabyte when each location stores one byte."
                ),
                "hint": "2 raised to the power of 20 gives 1 Megabyte."
            },

            {
                "id": 17,
                "question_text": (
                    "It holds instructions in hardware that can be changed "
                    "occasionally for later boots."
                ),
                "options": {
                    "A": "RAM",
                    "B": "ROM",
                    "C": "PROM",
                    "D": "EPROM"
                },
                "answer": "D",
                "explanation": (
                    "EPROM (Erasable Programmable Read-Only Memory) holds non-volatile "
                    "firmware that can be erased and reprogrammed occasionally."
                ),
                "hint": "Look for the type of ROM that can be erased and updated."
            },

            # --- SOFTWARE TESTING / ALGORITHMS QUESTIONS (18 to 34) ---

            {
                "id": 18,
                "question_text": (
                    "Which characteristic of an algorithm ensures that "
                    "it will eventually come to an end?"
                ),
                "options": {
                    "A": "Input",
                    "B": "Output",
                    "C": "Finiteness",
                    "D": "Iteration"
                },
                "answer": "C",
                "explanation": (
                    "An algorithm must be finite, meaning that it must "
                    "eventually terminate after a limited number of steps."
                ),
                "hint": "Think about whether the algorithm eventually stops."
            },

            {
                "id": 19,
                "question_text": (
                    "A variable declared inside a function can normally "
                    "be accessed only within that function. This is an "
                    "example of:"
                ),
                "options": {
                    "A": "Global scope",
                    "B": "Local scope",
                    "C": "Public access",
                    "D": "Inheritance"
                },
                "answer": "B",
                "explanation": (
                    "A variable declared inside a function normally has "
                    "local scope and can only be accessed within that function."
                ),
                "hint": "The variable is restricted to the function where it was declared."
            },

            {
                "id": 20,
                "question_text": (
                    "Two variables in a program can have the same name "
                    "without causing confusion when they are declared "
                    "in different:"
                ),
                "options": {
                    "A": "Data types",
                    "B": "Declarations",
                    "C": "Scopes",
                    "D": "Syntaxes"
                },
                "answer": "C",
                "explanation": (
                    "Variables with the same name can exist in different "
                    "scopes because each variable is accessible only within "
                    "its respective scope."
                ),
                "hint": "Think about where a variable can be accessed."
            },

            {
                "id": 21,
                "question_text": (
                    "Which type of testing checks whether individual "
                    "components or modules of a software system work correctly?"
                ),
                "options": {
                    "A": "Unit testing",
                    "B": "Acceptance testing",
                    "C": "System testing",
                    "D": "Installation testing"
                },
                "answer": "A",
                "explanation": (
                    "Unit testing tests individual software components "
                    "or modules to verify that they work correctly."
                ),
                "hint": "Think about testing one small component at a time."
            },

            {
                "id": 22,
                "question_text": (
                    "Which testing is performed to determine whether "
                    "a completed system meets the requirements of the customer or user?"
                ),
                "options": {
                    "A": "Unit testing",
                    "B": "Acceptance testing",
                    "C": "Syntax testing",
                    "D": "Component testing"
                },
                "answer": "B",
                "explanation": (
                    "Acceptance testing determines whether the completed "
                    "system satisfies the requirements and expectations "
                    "of the customer or end user."
                ),
                "hint": "The customer or end user is involved in this type of testing."
            },

            {
                "id": 23,
                "question_text": (
                    "Which document provides instructions for installing "
                    "a software application on a computer?"
                ),
                "options": {
                    "A": "Test plan",
                    "B": "Installation manual",
                    "C": "Technical specification",
                    "D": "Source code"
                },
                "answer": "B",
                "explanation": (
                    "An installation manual provides instructions and "
                    "procedures for installing software correctly."
                ),
                "hint": "Look for the document specifically concerned with installation."
            },

            {
                "id": 24,
                "question_text": (
                    "Which testing is mainly concerned with checking "
                    "whether a program produces the expected results for given inputs?"
                ),
                "options": {
                    "A": "Functional testing",
                    "B": "Installation testing",
                    "C": "Recovery testing",
                    "D": "Security testing"
                },
                "answer": "A",
                "explanation": (
                    "Functional testing checks whether the software "
                    "functions according to its specified requirements "
                    "and produces the expected results."
                ),
                "hint": "Think about whether the software performs its required functions."
            },

            {
                "id": 25,
                "question_text": (
                    "Which of the following is an important characteristic "
                    "of a good algorithm?"
                ),
                "options": {
                    "A": "It must be ambiguous",
                    "B": "It must have infinite steps",
                    "C": "Its instructions must be clear and unambiguous",
                    "D": "It must contain errors"
                },
                "answer": "C",
                "explanation": (
                    "A good algorithm must contain clear and unambiguous "
                    "instructions so that each step can be understood and executed correctly."
                ),
                "hint": "Each instruction should have only one clear meaning."
            },

            {
                "id": 26,
                "question_text": (
                    "What is the main purpose of a flowchart in software development?"
                ),
                "options": {
                    "A": "To store data permanently",
                    "B": "To graphically represent the steps of an algorithm",
                    "C": "To compile source code",
                    "D": "To encrypt information"
                },
                "answer": "B",
                "explanation": (
                    "A flowchart uses standard symbols and arrows to "
                    "graphically represent the sequence and logic of an algorithm or process."
                ),
                "hint": "It is a diagram used to show the steps of a process."
            },

            {
                "id": 27,
                "question_text": (
                    "Which software development activity involves examining "
                    "the source code to identify errors and defects?"
                ),
                "options": {
                    "A": "Code review",
                    "B": "Data entry",
                    "C": "Data compression",
                    "D": "File formatting"
                },
                "answer": "A",
                "explanation": (
                    "A code review involves examining source code to "
                    "identify defects, errors, security problems and possible improvements."
                ),
                "hint": "Developers inspect the code before or during testing."
            },

            {
                "id": 28,
                "question_text": (
                    "What is the main purpose of software maintenance?"
                ),
                "options": {
                    "A": "To prevent users from accessing software",
                    "B": "To modify and improve software after deployment",
                    "C": "To delete all existing programs",
                    "D": "To replace the computer hardware"
                },
                "answer": "B",
                "explanation": (
                    "Software maintenance involves modifying software "
                    "after deployment to correct faults, improve performance "
                    "or adapt it to changing requirements."
                ),
                "hint": "Maintenance happens after software has been deployed."
            },

            {
                "id": 29,
                "question_text": (
                    "Which type of error occurs when a program violates "
                    "the rules of a programming language?"
                ),
                "options": {
                    "A": "Logic error",
                    "B": "Syntax error",
                    "C": "Runtime result",
                    "D": "Hardware error"
                },
                "answer": "B",
                "explanation": (
                    "A syntax error occurs when code does not follow the "
                    "rules and structure required by the programming language."
                ),
                "hint": "Think about the grammar or rules of a programming language."
            },

            {
                "id": 30,
                "question_text": (
                    "A program runs successfully but produces the wrong "
                    "answer because the programmer used an incorrect formula. "
                    "What type of error is this?"
                ),
                "options": {
                    "A": "Syntax error",
                    "B": "Logic error",
                    "C": "Compilation error",
                    "D": "Installation error"
                },
                "answer": "B",
                "explanation": (
                    "A logic error occurs when a program executes but "
                    "produces an incorrect result because the underlying logic is wrong."
                ),
                "hint": "The program runs, but the result is incorrect."
            },

            {
                "id": 31,
                "question_text": (
                    "Which testing technique checks how a software "
                    "application behaves when incorrect or unexpected input is supplied?"
                ),
                "options": {
                    "A": "Boundary testing",
                    "B": "Stress testing",
                    "C": "Input validation testing",
                    "D": "Installation testing"
                },
                "answer": "C",
                "explanation": (
                    "Input validation testing checks whether a program "
                    "properly handles valid, invalid and unexpected input."
                ),
                "hint": "The focus is on checking what happens when users enter unexpected data."
            },

            {
                "id": 32,
                "question_text": (
                    "Which document describes what a software testing "
                    "process will test, how it will be tested and the resources required?"
                ),
                "options": {
                    "A": "Test plan",
                    "B": "Installation manual",
                    "C": "User password",
                    "D": "Source code"
                },
                "answer": "A",
                "explanation": (
                    "A test plan describes the testing objectives, scope, "
                    "approach, resources and activities required for testing a software system."
                ),
                "hint": "It is a plan specifically prepared for testing."
            },

            {
                "id": 33,
                "question_text": (
                    "Which of the following is NOT normally considered "
                    "a software testing activity?"
                ),
                "options": {
                    "A": "Finding defects",
                    "B": "Checking requirements",
                    "C": "Verifying expected results",
                    "D": "Increasing monitor brightness"
                },
                "answer": "D",
                "explanation": (
                    "Increasing monitor brightness is a hardware/display "
                    "setting and is not a normal software testing activity."
                ),
                "hint": "Choose the option that is unrelated to software testing."
            },

            {
                "id": 34,
                "question_text": (
                    "A programmer executes a program with different sets "
                    "of input data to determine whether it behaves correctly. "
                    "This process is called:"
                ),
                "options": {
                    "A": "Testing",
                    "B": "Compilation",
                    "C": "Encryption",
                    "D": "Compression"
                },
                "answer": "A",
                "explanation": (
                    "Software testing involves executing a program with "
                    "different inputs and checking whether the actual "
                    "results match the expected results."
                ),
                "hint": "It is the process of checking whether software works."
            }

        ]
    }