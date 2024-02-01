"use client";
import useWebSocket, { ReadyState } from "react-use-websocket";
import { useEffect, useState } from "react";
import { Button } from "../ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import ChatMessage from "./message";
import useUser from "@/hooks/user";
import { Loader2Icon, Wifi } from "lucide-react";
import CreateMessageForm from "./create-message-form";
import { ScrollArea } from "@/components/ui/scroll-area";

const Chat = () => {
  const wsUrl = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8080/ws";
  const { authenticated, access_token } = useUser();
  const [socketUrl, setSocketUrl] = useState(wsUrl);
  const [messages, setMessages] = useState(null);
  const {
    sendMessage,
    sendJsonMessage,
    lastMessage,
    lastJsonMessage,
    readyState,
    getWebSocket,
  } = useWebSocket(socketUrl, {
    onError(event) {
      console.log(event);
    },
    onMessage(event) {
      console.log(socketUrl);
      console.log(event);
      const eventData = JSON.parse(event.data);
      switch (eventData.event) {
        case "get_messages":
          setMessages(eventData.data);
          console.log(messages);
          break;
        case "get_message":
          console.log(`New message -> ${eventData.data}`);
          break;
      }
    },
    onOpen: () => {
      console.log(wsUrl);
      console.log("Polaczono");
      sendJsonMessage({
        event: "get_messages",
      });
    },
    //Will attempt to reconnect on all close events, such as server shutting down
    shouldReconnect: (closeEvent) => true,
  });

  useEffect(() => {
    if (authenticated && access_token)
      setSocketUrl(`${wsUrl}?token=${access_token.token}`);
  }, [authenticated, access_token]);

  const connectionStatus = {
    [ReadyState.CONNECTING]: (
      <span>
        <Loader2Icon className="animate-spin ml-2 h-2 w-2 align-middle mt-2 float-right" />
      </span>
    ),
    [ReadyState.OPEN]: (
      <span className="animate-ping ml-2 h-2 w-2 align-middle mt-2 rounded-full bg-green-400 opacity-75 float-right "></span>
    ),
    [ReadyState.CLOSING]: (
      <span className="animate-ping ml-2 h-2 w-2 align-middle mt-2 rounded-full bg-red-400 opacity-75 float-right "></span>
    ),
    [ReadyState.CLOSED]: (
      <span className="ml-2 h-2 w-2 align-middle mt-2 rounded-full bg-red-400 opacity-75 float-right "></span>
    ),
    [ReadyState.UNINSTANTIATED]: "Uninstantiated",
  }[readyState];

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex">Chat {connectionStatus}</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col">
        <ScrollArea className="h-[350px]">
          {messages &&
            messages?.items.map((item, i) => <ChatMessage key={i} {...item} />)}
        </ScrollArea>

        {authenticated && (
          <CreateMessageForm sendJsonMessage={sendJsonMessage} />
        )}
      </CardContent>
    </Card>
  );
};

export default Chat;
