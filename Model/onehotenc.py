import midi
import numpy as np
import matplotlib.pyplot as plt
import pickle
import io
import json

# Comverts MIDI file pattern to representation of notes events in absolute time
class NoteEvents:
    def __init__(self, song, note_tracks=None, start_on_note=True):
        self._event_list = []
        self.note_time_list = []
        self.pattern = midi.read_midifile (song)
        self.pattern.make_ticks_abs ( )
        self.ticks_per_beat = self.pattern.resolution
        self.numNotes = 88
        # offset between note index and MIDI note number
        self.noteOffset = 9
        self.PPQ = 480
        # list of track names to include notes from
        self.note_tracks = note_tracks
        self.start_on_note = start_on_note
        self._parse_events()


    def _parse_events(self):
        for i in range(len(self.pattern)):
            for event in self.pattern[i]:
                if type(event) in (midi.events.NoteOnEvent, midi.events.NoteOffEvent):
                    self._event_list.append(event)
                elif type(event) == midi.events.SetTempoEvent:
                    self._event_list.append(event)
                elif type(event) == midi.events.EndOfTrackEvent and event.tick != 0:
                    self._event_list.append(event)
        self._event_list_timed()


    def _event_list_timed(self):
        assert(type(self._event_list[0]) == midi.events.SetTempoEvent)
        microseconds_per_beat = self._event_list[0].get_mpqn()

        prev_time = 0
        prev_tick = 0
        microseconds_per_tick = float(microseconds_per_beat) / self.PPQ
        for event in self._event_list:

            tick_diff = event.tick - prev_tick

            curr_time = prev_time + (tick_diff * microseconds_per_tick)
            if type(event) != midi.events.SetTempoEvent:
                self.note_time_list.append((event, curr_time))
                prev_time = curr_time
                prev_tick = event.tick

        start_time = self.note_time_list[0][1]

        if self.start_on_note:
            for i, tup in enumerate(self.note_time_list):
                self.note_time_list[i] = (tup[0],tup[1]-start_time)
        self._last_event_time = self.note_time_list[-1][1]


    def _note_off(self, note_event):
        return ((type(note_event) == midi.events.NoteOnEvent) and (note_event.get_velocity() == 0)) \
                    or type(note_event) == midi.events.NoteOffEvent

    # returns index of first slice at or after given time
    # time in microseconds
    def time_to_slice(self, t, slices_per_second):
        microseconds_per_slice = 1e6 / slices_per_second
        return np.ceil(float(t) / microseconds_per_slice).astype(int)

    # duration in seconds
    def get_ground_truth(self, slices_per_second, duration=None):

        microseconds_per_slice = 1e6 / slices_per_second
        number_slices = np.ceil(self._last_event_time / microseconds_per_slice).astype(int)
        ground_truth = np.zeros(self.numNotes * number_slices).reshape(self.numNotes, number_slices)
        template = np.zeros(self.numNotes).reshape(self.numNotes,1)

        prev_time = 0
        for note, curr_time in self.note_time_list:
           # print(curr_time)
            if prev_time != curr_time:
                prev_time_slice = self.time_to_slice(prev_time, slices_per_second)
                curr_time_slice = self.time_to_slice(curr_time, slices_per_second)
                #make all slices in [prev_time, curr_time) equal to current template
                ground_truth[:,prev_time_slice:curr_time_slice] = template.repeat(curr_time_slice - prev_time_slice, axis=1)


            pitch_index = 0

            if type(note) != midi.events.EndOfTrackEvent:
                pitch_index = note.get_pitch() - self.noteOffset

            if pitch_index > 0 and pitch_index < self.numNotes:
                if self._note_off(note):
                    template[pitch_index] = 0
                else:
                    template[pitch_index] = 1

            prev_time = curr_time
        if duration != None:
            ground_truth = ground_truth[:,:self.time_to_slice(1e6 * duration, slices_per_second)]
        return ground_truth


def getHotVector(song,samplingFReq,duration):
    events = NoteEvents(song)
    truth = events.get_ground_truth(samplingFReq,duration)
    print(truth.shape)
    np.savetxt ( "foo.csv", truth, delimiter="," )
    memfile = io.BytesIO()
    np.save(memfile, truth)
    memfile.seek(0)
    serialized = json.dumps(memfile.read().decode('latin-1'))
    return serialized

if __name__ == '__main__':
    truth = getHotVector('ddrum.midi',31.25,20)
    #plt.matshow(truth)
    #plt.show()
