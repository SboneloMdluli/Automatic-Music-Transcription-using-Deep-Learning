import midi
import numpy as np
import matplotlib.pyplot as plt


# Comverts MIDI file pattern to representation of notes events in absolute time
class NoteEvents:
    def __init__(self, pattern, note_tracks=None, start_on_note=True):
        self._event_list = []
        self.note_time_list = []
        pattern.make_ticks_abs()
        self.pattern = pattern
        self.ticks_per_beat = pattern.resolution
        self.numNotes = 88
        # offset between note index and MIDI note number
        self.noteOffset = 9
        # list of track names to include notes from
        self.note_tracks = note_tracks
        self.names = self._name_tracks()
        self.start_on_note = start_on_note
        self._parse_events()

    def _name_tracks(self):
        names = [None] * len(self.pattern)
        for i in range(len(self.pattern)):
            for event in self.pattern[i]:
                if type(event) == midi.events.TrackNameEvent:
                    names[i] = event.text
                break
        return names

    def _parse_events(self):
        for i in range(len(self.pattern)):
            for event in self.pattern[i]:
                if type(event) in (midi.events.NoteOnEvent, midi.events.NoteOffEvent):
                    if self.note_tracks == None or self.names[i] in self.note_tracks:
                        self._event_list.append(event)
                elif type(event) == midi.events.SetTempoEvent:
                    self._event_list.append(event)
                elif type(event) == midi.events.EndOfTrackEvent and event.tick != 0:
                    self._event_list.append(event)
        self._event_list = sorted(self._event_list, key=lambda x: x.tick)
        self._event_list_timed()


    def _event_list_timed(self):
        assert(type(self._event_list[0]) == midi.events.SetTempoEvent)
        microseconds_per_beat = self._event_list[0].get_mpqn()

        prev_time = 0
        prev_tick = 0
        microseconds_per_tick = float(microseconds_per_beat) / self.ticks_per_beat
        for event in self._event_list:
            tick_diff = event.tick - prev_tick
            curr_time = prev_time + (tick_diff * microseconds_per_tick)
            if type(event) != midi.events.SetTempoEvent:
                self.note_time_list.append((event, curr_time))
                prev_time = curr_time
                prev_tick = event.tick
            else:
                prev_time = curr_time
                prev_tick = event.tick
                microseconds_per_beat = event.get_mpqn()
                microseconds_per_tick = float(microseconds_per_beat) / self.ticks_per_beat
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
            if prev_time != curr_time:
                prev_time_slice = self.time_to_slice(prev_time, slices_per_second)
                curr_time_slice = self.time_to_slice(curr_time, slices_per_second)
                #make all slices in [prev_time, curr_time) equal to current template
                ground_truth[:,prev_time_slice:curr_time_slice] = template.repeat(curr_time_slice - prev_time_slice, axis=1)

            pitch_index = 0
            if type(note) != midi.events.EndOfTrackEvent:
                pitch_index = note.get_pitch() - self.noteOffset
                print(note.get_pitch() )

            if pitch_index >= 0 and pitch_index < self.numNotes:
                if self._note_off(note):
                    template[pitch_index] = 0
                else:
                    template[pitch_index] = 1
            prev_time = curr_time
        if duration != None:
            ground_truth = ground_truth[:,:self.time_to_slice(1e6 * duration, slices_per_second)]
        return ground_truth



if __name__ == '__main__':
    pattern = midi.read_midifile('vss.midi')
    events = NoteEvents(pattern)
    truth = events.get_ground_truth(31.25, 20)


    plt.matshow(truth)
    plt.show()

