test = ['Jan 6th', 'Jan 8th', 'Course Overview and Logistics', 'Neurons and the Central Nervous System', 'Jan 13th', 'Jan 22nd', 'Simple Neuron Models', 'Hodgkin-Huxley Models', 'Compartmental Models', 'Synapses', 'Jan 27th', 'Feb 5th', 'Low-level Visual Processing', 'Perceptrons and Regression', 'Intermediate and High-level Visual Processing', 'Backpropagation and Convolutional Neural Networks', 'Feb 10th', 'Feb 24th', 'Role in cognition and associated signalling', 'Modelling memory', 'Modelling spatial navigation', 'Feb 26th', 'Mar 5th', 'Role in Cognition and Associated Signalling', 'Models of BG - Functional', 'Models of BG - Anatomical', 'Reinforcement Learning', 'Mar 10th', 'Mar 12th', 'The Motor Cortex', 'The Cerebellum', 'Mar 17th', 'Apr 2nd', 'The Neural Engineering Framework', 'Numerical Cognition', 'Fear Conditioning in Amygdala', 'Recurrent Networks and Working Memory', 'Biophysics of Drugs and Disorders', 'Higher-level Cognition']

months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

start_dates = []

if any(month in test[i].lower() for month in months) and any(month in test[i+1].lower() for month in months):
    start_dates.append(i)