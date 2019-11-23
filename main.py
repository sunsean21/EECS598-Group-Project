from device import Device, TouchScreenKeyboardDeviceDirector
from human import Human, Eyes, Finger
from operators import OperatorElement, Perceptual, Encode, Cognitive, RetrieveTargetLocation, ActivateTargetLocation, MotorOperator, Move
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
import sys

# This is the main function that runs all your  simulations and predicitons.
# Use this to execute your simulation.
# Contributors: nbanovic@umich.edu, jspalt@umich.edu
	

def main(argv):

	# Constructs a sample touchscreen device with keyboard at the bottom third of the device.
	device = TouchScreenKeyboardDeviceDirector.construct('device', 'device', 0, 0, 2600, 1010, 0, 0)

	# Create a human and associate it with the device, so that the device knows about any body part movements.
	# human = Human.create_novice(device)
	human = Human.create_expert(device) # TODO: to test your  implementation with an expert user, uncomment this line and comment the one above it.

	phrase_textbox = device.find_descendant('phrase_textbox')
	space_key = device.find_descendant(' ')

	transcription_textbox = device.find_descendant('transcription_textbox')

	# Reset the thumb to the space before each phrase.
	human.body_parts['thumb'].location_x = space_key.top_left_x + space_key.width/2
	human.body_parts['thumb'].location_y = space_key.top_left_y + space_key.height/2

	# Reset the eyes to the phrase text box.
	human.body_parts['eyes'].fixation_x = phrase_textbox.top_left_x + phrase_textbox.width/2
	human.body_parts['eyes'].fixation_y = phrase_textbox.top_left_y + phrase_textbox.height/2


	#  Visualize the device interface and the position of the thumb.
	device_plot = plt.figure()
	ax1 = device_plot.add_subplot(111, aspect='equal')
	ax1.xaxis.set_ticks(range(device.top_left_x, device.width, 200))
	ax1.yaxis.set_ticks(range(device.top_left_y, device.height, 200))

	device.draw(ax1)
	human.draw(ax1)
	
	plt.ylim((0, device.height))
	plt.xlim((0, device.width))
	ax1.set_ylim(ax1.get_ylim()[::-1]) 
	ax1.xaxis.tick_top()

	plt.show(block=True)
	plt.close()

	# Variables for computing average typing speed.
	total_characters_count = 0
	total_duration = 0.0

	phrase_typing_speeds = []
	phrase_typing_timestamps = []

'''
	# For each test phrase in the file compute the duration it takes to type that phrase.
	with open('data/phrases.txt') as phrase_set:
		for phrase in phrase_set:

			phrase_typing_timestamps.append(total_duration/(60.0*1000.0)) # start time for this phrase since the fist time typing in minutes.

			phrase = phrase.lower().rstrip()

			phrase_textbox = device.get_descendant('phrase_textbox')
			phrase_textbox.set_text(phrase)

			transcription_textbox = device.get_descendant('transcription_textbox')
			transcription_textbox.set_text('')

			# Reset the thumb to the space before each phrase.
			human.body_parts['thumb'].location_x = space_key.top_left_x + space_key.width/2
			human.body_parts['thumb'].location_y = space_key.top_left_y + space_key.height/2

			# Reset the eyes to the phrase text box.
			human.body_parts['eyes'].fixation_x = phrase_textbox.top_left_x + phrase_textbox.width/2
			human.body_parts['eyes'].fixation_y = phrase_textbox.top_left_y + phrase_textbox.height/2
			
			schedule_chart = human.press(phrase)

			duration = human.compute_duration(schedule_chart)

			total_characters_count += len(phrase)
			total_duration += duration

			human.timestamp_offset = total_duration

			current_speed_char_per_second = len(phrase)/(duration/1000.0)
			current_speed_words_per_minute = current_speed_char_per_second * 60/5

			phrase_typing_speeds.append(current_speed_words_per_minute)

			if len(phrase_typing_speeds) % 250 ==  0:
				human.draw_schedule_graph(phrase, schedule_chart)

				#  Visualize the typing speeds over time.
				plt.scatter(phrase_typing_timestamps, phrase_typing_speeds)
				plt.title('Typing speeds over time')
				plt.xlabel('Time (min)')
				plt.ylabel('Speed (WPM)')

				plt.show(block=True)
				plt.close()

	# Convert total_duration from milliseconds to seconds.
	total_duration /= 1000.0

	speed_char_per_second = total_characters_count/total_duration

	speed_words_per_minute = speed_char_per_second * 60/5

	print("Typists can enter text at the speed of " + str(speed_words_per_minute) + "WPM.")

'''
if __name__ == "__main__":
	main(sys.argv)

