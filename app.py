from transformers import pipeline
import streamlit as st

# Initialize Streamlit app
st.title("AI Event Planner with Hugging Face")
st.write("Generate ideas for your next event using Hugging Face's models!")

# Load Hugging Face model pipeline
generator = pipeline("text-generation", model="gpt2")

# Event Details Input
event_type = st.selectbox("Select the type of event:", ["Birthday", "Wedding", "Corporate", "Party", "Other"])
event_date = st.date_input("Select the event date:")
location = st.text_input("Enter the event location:")
guest_count = st.number_input("Estimated number of guests:", min_value=1, max_value=500, value=50)
theme = st.text_input("Preferred theme (optional):")
budget = st.number_input("Budget (optional):", min_value=0.0, format="%.2f")

# Function to generate event ideas using Hugging Face GPT-2
def generate_event_ideas(prompt):
    response = generator(prompt, max_length=150, num_return_sequences=1)
    return response[0]["generated_text"].strip()

# Variable to store the generated event plan
event_plan = ""

# Generate Event Plan
if st.button("Generate Event Plan"):
    prompt = (
        f"I am planning a {event_type.lower()} on {event_date} at {location} "
        f"with about {guest_count} guests. The theme is '{theme}' and the budget is {budget}. "
        "Please suggest ideas for decoration, activities, and a checklist."
    )

    with st.spinner("Generating event ideas..."):
        try:
            event_plan = generate_event_ideas(prompt)
            st.success("Here are your event suggestions:")
            st.write(event_plan)
        except Exception as e:
            st.error(f"Error generating event ideas: {e}")

# Save Event Plan
if st.button("Save Plan"):
    if event_plan:  # Check if event_plan has been generated
        with open("event_plan.txt", "w") as file:
            file.write(f"Event Plan for {event_type} on {event_date}\n\n{event_plan}")
        st.success("Your event plan has been saved as 'event_plan.txt'!")
    else:
        st.error("Please generate the event plan first before saving.")
