"use client";

import { CloseIcon } from "@/components/CloseIcon";
import { NoAgentNotification } from "@/components/NoAgentNotification";
import {
  AgentState,
  BarVisualizer,
  DisconnectButton,
  LiveKitRoom,
  RoomAudioRenderer,
  VoiceAssistantControlBar,
  useVoiceAssistant
} from "@livekit/components-react";
import { useKrispNoiseFilter } from "@livekit/components-react/krisp";
import { AnimatePresence, motion } from "framer-motion";
import { MediaDeviceFailure } from "livekit-client";
import { useCallback, useEffect, useState } from "react";
import type { ConnectionDetails } from "./api/connection-details/route";

import { TranscriptionSegment, Participant, RoomEvent } from "livekit-client";
import { useRoomContext } from "@livekit/components-react";

interface EnhancedTranscriptionSegment {
  segment: TranscriptionSegment;
  participantIdentity?: string;
}

interface TranscriptionSidebarProps {
  isOpen: boolean;
  toggleSidebar: () => void;
}

interface ControlBarProps {
  onConnectButtonClicked: () => void;
  agentState: AgentState;
  toggleSidebar: () => void;
  sidebarOpen: boolean;
}

export default function Page() {
  const [connectionDetails, updateConnectionDetails] = useState<ConnectionDetails | undefined>(undefined);
  const [agentState, setAgentState] = useState<AgentState>("disconnected");
  const [sidebarOpen, setSidebarOpen] = useState<boolean>(false);

  const toggleSidebar = useCallback(() => {
    setSidebarOpen(prev => !prev);
  }, []);

  const onConnectButtonClicked = useCallback(async () => {
    // Generate room connection details, including:
    //   - A random Room name
    //   - A random Participant name
    //   - An Access Token to permit the participant to join the room
    //   - The URL of the LiveKit server to connect to
    //
    // In real-world application, you would likely allow the user to specify their
    // own participant name, and possibly to choose from existing rooms to join.

    const url = new URL(
      process.env.NEXT_PUBLIC_CONN_DETAILS_ENDPOINT ?? "/api/connection-details",
      window.location.origin
    );
    const response = await fetch(url.toString());
    const connectionDetailsData = await response.json();
    updateConnectionDetails(connectionDetailsData);
  }, []);

  return (
    <main data-lk-theme="default" className="h-full grid content-center bg-[var(--lk-bg)]">
      <LiveKitRoom
        token={connectionDetails?.participantToken}
        serverUrl={connectionDetails?.serverUrl}
        connect={connectionDetails !== undefined}
        audio={true}
        video={false}
        onMediaDeviceFailure={onDeviceFailure}
        onDisconnected={() => {
          updateConnectionDetails(undefined);
        }}
        className="grid grid-rows-[2fr_1fr] items-center"
      >
        <SimpleVoiceAssistant onStateChange={setAgentState} />
        <ControlBar 
          onConnectButtonClicked={onConnectButtonClicked} 
          agentState={agentState} 
          toggleSidebar={toggleSidebar}
          sidebarOpen={sidebarOpen}
        />
        <RoomAudioRenderer />
        <NoAgentNotification state={agentState} />
        <TranscriptionSidebar isOpen={sidebarOpen} toggleSidebar={toggleSidebar} />
      </LiveKitRoom>
    </main>
  );
}

function TranscriptionSidebar({ isOpen, toggleSidebar }: TranscriptionSidebarProps) {
  const room = useRoomContext();
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
    <div className={`transcription-sidebar fixed right-0 top-0 h-full bg-[var(--lk-bg)] border-l border-white/10 w-80 transition-transform duration-300 z-50 ${isOpen ? 'translate-x-0' : 'translate-x-full'}`}>
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
              const isAgent = !participantIdentity || participantIdentity === 'agent';
              
              return (
                <li key={segment.id} className={`${isAgent ? 'pl-2' : 'pr-2'}`}>
                  <div className={`p-3 rounded-lg max-w-[90%] ${isAgent ? 'bg-blue-900/30 ml-0 mr-auto' : 'bg-green-900/30 ml-auto mr-0'} ${segment.final ? 'opacity-100' : 'opacity-70'}`}>
                    <p className={`text-sm font-semibold mb-1 ${isAgent ? 'text-blue-300' : 'text-green-300'}`}>
                      {isAgent ? 'Culinary Vertex' : 'You'}
                    </p>
                    <p className="text-white">{segment.text}</p>
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

function SimpleVoiceAssistant(props: { onStateChange: (state: AgentState) => void }) {
  const { state, audioTrack } = useVoiceAssistant();
  useEffect(() => {
    props.onStateChange(state);
  }, [props, state]);
  return (
    <div className="flex flex-col items-center h-[300px] max-w-[90vw] mx-auto">
      <BarVisualizer
        state={state}
        barCount={5}
        trackRef={audioTrack}
        className="agent-visualizer mb-4"
        options={{ minHeight: 24 }}
      />
    </div>
  );
}

function ControlBar({ onConnectButtonClicked, agentState, toggleSidebar, sidebarOpen }: ControlBarProps) {
  /**
   * Use Krisp background noise reduction when available.
   * Note: This is only available on Scale plan, see {@link https://livekit.io/pricing | LiveKit Pricing} for more details.
   */
  const krisp = useKrispNoiseFilter();
  useEffect(() => {
    krisp.setNoiseFilterEnabled(true);
  }, [krisp]);

  return (
    <div className="relative h-[100px]">
      <AnimatePresence>
        {agentState === "disconnected" && (
          <motion.button
            initial={{ opacity: 0, top: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0, top: "-10px" }}
            transition={{ duration: 1, ease: [0.09, 1.04, 0.245, 1.055] }}
            className="uppercase absolute left-1/2 -translate-x-1/2 px-4 py-2 bg-white text-black rounded-md"
            onClick={() => onConnectButtonClicked()}
          >
            Start a conversation
          </motion.button>
        )}
      </AnimatePresence>
      <AnimatePresence>
        {agentState !== "disconnected" && agentState !== "connecting" && (
          <motion.div
            initial={{ opacity: 0, top: "10px" }}
            animate={{ opacity: 1, top: 0 }}
            exit={{ opacity: 0, top: "-10px" }}
            transition={{ duration: 0.4, ease: [0.09, 1.04, 0.245, 1.055] }}
            className="flex h-8 absolute left-1/2 -translate-x-1/2 justify-center items-center space-x-2"
          >
            <VoiceAssistantControlBar controls={{ leave: false }} />
            <button 
              onClick={toggleSidebar}
              className={`px-2 py-1 text-xs rounded ${sidebarOpen ? 'bg-blue-500 text-white' : 'bg-white/10 text-white/80 hover:bg-white/20'}`}
            >
              {sidebarOpen ? 'Hide Transcript' : 'Show Transcript'}
            </button>
            <DisconnectButton>
              <CloseIcon />
            </DisconnectButton>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

// Define the overlay that appears when there is an issue capturing the microphone
function onDeviceFailure(error?: MediaDeviceFailure) {
  console.error(error);
  alert(
    "Error acquiring microphone permissions. Please make sure you grant the necessary permissions in your browser and reload the tab"
  );
}
