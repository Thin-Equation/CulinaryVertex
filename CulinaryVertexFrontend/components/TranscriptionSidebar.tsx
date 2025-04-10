import { useState, useEffect } from "react";
import { CloseIcon } from "@/components/CloseIcon";
import { TranscriptionSegment, Participant, RoomEvent } from "livekit-client";
import { useRoomContext, useLocalParticipant } from "@livekit/components-react";

interface EnhancedTranscriptionSegment {
  segment: TranscriptionSegment;
  participantIdentity?: string;
}

interface TranscriptionSidebarProps {
  isOpen: boolean;
  toggleSidebar: () => void;
}

export default function TranscriptionSidebar({ isOpen, toggleSidebar }: TranscriptionSidebarProps) {
  const room = useRoomContext();
  const localParticipant = useLocalParticipant();
  const [transcriptions, setTranscriptions] = useState<Record<string, EnhancedTranscriptionSegment>>({});

  useEffect(() => {
    if (!room) return;

    const handleTranscriptionReceived = (
      segments: TranscriptionSegment[],
      participant?: Participant
    ) => {
      setTranscriptions((prev) => {
        const newTranscriptions = { ...prev };
        for (const segment of segments) {
          newTranscriptions[segment.id] = {
            segment,
            participantIdentity: participant?.identity
          };
        }
        return newTranscriptions;
      });
    };

    room.on(RoomEvent.TranscriptionReceived, handleTranscriptionReceived);
    
    return () => {
      room.off(RoomEvent.TranscriptionReceived, handleTranscriptionReceived);
    };
  }, [room]);

  // Sort transcriptions by time received
  const sortedSegments = Object.values(transcriptions)
    .sort((a, b) => a.segment.firstReceivedTime - b.segment.firstReceivedTime);

  return (
    <div className={`transcription-sidebar fixed right-0 top-16 h-[calc(100%-64px)] bg-[var(--lk-bg)] border-l border-white/10 w-80 transition-transform duration-300 z-50 ${isOpen ? 'translate-x-0' : 'translate-x-full'}`}>
      <div className="flex justify-between items-center p-4 border-b border-white/10">
        <h3 className="text-white font-semibold">Conversation Transcript</h3>
        <button onClick={toggleSidebar} className="text-white/70 hover:text-white">
          <CloseIcon />
        </button>
      </div>
      
      <div className="p-4 h-[calc(100%-64px)] overflow-y-auto">
        {sortedSegments.length > 0 ? (
          <ul className="space-y-4">
            {sortedSegments.map(({ segment, participantIdentity }) => {
              // Determine if this is the local participant (user) based on identity comparison
              const isUser = participantIdentity === localParticipant.localParticipant.identity;
              
              return (
                <li key={segment.id} className={`${isUser ? 'pr-2' : 'pl-2'}`}>
                  <div className={`p-3 rounded-lg max-w-[90%] ${isUser ? 'bg-green-900/30 ml-auto mr-0' : 'bg-blue-900/30 ml-0 mr-auto'} ${segment.final ? 'opacity-100' : 'opacity-70'}`}>
                    <p className={`text-sm font-semibold mb-1 ${isUser ? 'text-green-300' : 'text-blue-300'}`}>
                      {isUser ? 'You' : 'Culinary Vertex'}
                    </p>
                    <p className="text-white">
                      {segment.final ? segment.text : `${segment.text} ...`}
                    </p>
                  </div>
                </li>
              );
            })}
          </ul>
        ) : (
          <p className="text-white/50 text-center italic mt-4">Your conversation will appear here</p>
        )}
      </div>
    </div>
  );
}
