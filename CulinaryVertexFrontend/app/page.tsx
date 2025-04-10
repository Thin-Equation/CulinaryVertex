"use client";

import { CloseIcon } from "@/components/CloseIcon";
// import { NoAgentNotification } from "@/components/NoAgentNotification";
import Header from "@/components/Header";
import MenuSidebar from "@/components/MenuSidebar";
import TranscriptionSidebar from "@/components/TranscriptionSidebar";
import {
  AgentState,
  BarVisualizer,
  DisconnectButton,
  LiveKitRoom,
  RoomAudioRenderer,
  VoiceAssistantControlBar,
  useVoiceAssistant
} from "@livekit/components-react";
import { AnimatePresence, motion } from "framer-motion";
import { MediaDeviceFailure } from "livekit-client";
import { useCallback, useEffect, useState } from "react";
import type { ConnectionDetails } from "./api/connection-details/route";

interface ControlBarProps {
  onConnectButtonClicked: () => void;
  agentState: AgentState;
  toggleTranscriptSidebar: () => void;
  toggleMenuSidebar: () => void;
  transcriptSidebarOpen: boolean;
  menuSidebarOpen: boolean;
}

export default function Page() {
  const [connectionDetails, updateConnectionDetails] = useState<ConnectionDetails | undefined>(undefined);
  const [agentState, setAgentState] = useState<AgentState>("disconnected");
  const [transcriptSidebarOpen, setTranscriptSidebarOpen] = useState<boolean>(false);
  const [menuSidebarOpen, setMenuSidebarOpen] = useState<boolean>(false);

  const toggleTranscriptSidebar = useCallback(() => {
    setTranscriptSidebarOpen(prev => !prev);
  }, []);

  const toggleMenuSidebar = useCallback(() => {
    setMenuSidebarOpen(prev => !prev);
  }, []);

  const onConnectButtonClicked = useCallback(async () => {
    const url = new URL(
      process.env.NEXT_PUBLIC_CONN_DETAILS_ENDPOINT ?? "/api/connection-details",
      window.location.origin
    );
    const response = await fetch(url.toString());
    const connectionDetailsData = await response.json();
    updateConnectionDetails(connectionDetailsData);
  }, []);

  return (
    <main data-lk-theme="default" className="h-full bg-[var(--lk-bg)]">
      <Header />
      <div className="pt-16"> {/* Add padding top for fixed header */}
        <MenuSidebar isOpen={menuSidebarOpen} toggleSidebar={toggleMenuSidebar} />
        <div className={`transition-all duration-300 
          ${menuSidebarOpen ? 'ml-80' : 'ml-0'} 
          ${transcriptSidebarOpen ? 'mr-80' : 'mr-0'}`}
        >
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
              toggleTranscriptSidebar={toggleTranscriptSidebar}
              toggleMenuSidebar={toggleMenuSidebar}
              transcriptSidebarOpen={transcriptSidebarOpen}
              menuSidebarOpen={menuSidebarOpen}
            />
            <RoomAudioRenderer />
            {/* <NoAgentNotification state={agentState} /> */}
            <TranscriptionSidebar isOpen={transcriptSidebarOpen} toggleSidebar={toggleTranscriptSidebar} />
          </LiveKitRoom>
        </div>
      </div>
    </main>
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

function ControlBar({ 
  onConnectButtonClicked, 
  agentState, 
  toggleTranscriptSidebar, 
  toggleMenuSidebar,
  transcriptSidebarOpen,
  menuSidebarOpen 
}: ControlBarProps) {
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
              onClick={toggleMenuSidebar}
              className={`px-2 py-1 text-xs rounded ${menuSidebarOpen ? 'bg-amber-600 text-white' : 'bg-white/10 text-white/80 hover:bg-white/20'}`}
            >
              {menuSidebarOpen ? 'Hide Menu' : 'View Menu'}
            </button>
            <button 
              onClick={toggleTranscriptSidebar}
              className={`px-2 py-1 text-xs rounded ${transcriptSidebarOpen ? 'bg-blue-500 text-white' : 'bg-white/10 text-white/80 hover:bg-white/20'}`}
            >
              {transcriptSidebarOpen ? 'Hide Transcript' : 'Show Transcript'}
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

function onDeviceFailure(error?: MediaDeviceFailure) {
  console.error(error);
  alert(
    "Error acquiring microphone permissions. Please make sure you grant the necessary permissions in your browser and reload the tab"
  );
}
