"use client";
import { Page_PostOut_, ThreadOut } from "sharkservers-sdk";
import useCategory from "@/hooks/category";
import { useEffect, useState } from "react";
import useApi from "@/hooks/api";
import dynamic from "next/dynamic";

const Separator = dynamic(
  () => import("../ui/separator").then((mod) => mod.Separator),
  { ssr: false },
);
const Pagination = dynamic(() => import("../pagination").then((mod) => mod), {
  ssr: false,
});
const MarkdownPreview = dynamic(
  () => import("@uiw/react-markdown-preview").then((mod) => mod),
  { ssr: false },
);
const ThreadDetailActionMenu = dynamic(
  () => import("./thread-detail-action-menu").then((mod) => mod),
  { ssr: false },
);
const ThreadDetailCreatePost = dynamic(
  () => import("./thread-detail-create-post").then((mod) => mod),
  { ssr: false },
);
const UserInfo = dynamic(
  () => import("../users/user-info").then((mod) => mod),
  { ssr: false },
);
const ThreadBadges = dynamic(
  () => import("./thread-badges").then((mod) => mod),
  { ssr: false },
);
const Post = dynamic(() => import("./post").then((mod) => mod), { ssr: false });

interface IThreadDetail {
  thread: ThreadOut;
  posts: Page_PostOut_;
}

export default function ThreadDetail({ thread, posts }: IThreadDetail) {
  const {
    id,
    title,
    content,
    author,
    created_at,
    post_count,
    category,
    is_closed,
    is_pinned,
    meta_fields,
    status,
    server,
  } = thread;
  const { isApplicationCategory } = useCategory();
  const api = useApi();

  async function getServerId(meta_fields: any) {
    let serverId;
    meta_fields.map((field, i) => {
      if (field.name == "server_id") {
        serverId = field.value;
      }
    });
    return Number(serverId);
  }

  const meta_name_fields = ["question_experience", "question_reason"];
  return (
    <div className="rounded-[0.5rem] bg-background shadow">
      <div className="space-y-6 p-10 md:block">
        <div className="space-y-0.5">
          <h2 className="text-2xl font-bold tracking-tight">{title}</h2>
          <ThreadBadges
            categoryName={category?.name}
            is_closed={is_closed}
            is_pinned={is_pinned}
            serverName={server ? server.name : ""}
            status={isApplicationCategory(category) ? status : undefined}
          />
        </div>
        <Separator />
      </div>
      <div className="p-10 w-full flex flex-col md:flex-row gap-10 border">
        <div className="flex flex-col items-center w-full md:w-1/6  rounded-[0.5rem]  p-4 text-center h-[250px]">
          <UserInfo user={...author} avatarClassName="h-15 w-15  mx-auto" />
        </div>
        <div className="flex flex-col rounded-[0.5rem] p-2 w-full">
          <div className="ml-auto flex w-full justify-between">
            <div className="w-full">
              {/* {isApplicationCategory(category) ? (
                                <div className="flex flex-col">
                                    <span>Nick: {author.username}</span>
                                    {meta_fields && meta_fields.map((meta, i) =>
                                        <>
                                            {meta.name == "server_id" && server && (
                                                <h2>Serwer: {server.name}</h2>
                                            )}
                                            {meta.name == "question_age" && (
                                                <>
                                                    <h2>Wiek: {meta.value}</h2>
                                                </>
                                            )}
                                            {meta_name_fields.includes(meta.name) && (
                                                <>
                                                    {
                                                        meta.name == "question_reason" ? "Dlaczego chcesz zostac Administarorem?" : meta.name
                                                            ||
                                                            meta.name == "question_experience" ? "Doświadczenie" : meta.name
                                                    }: <MarkdownPreview source={meta.value} />
                                                </>
                                            )}

                                        </>

                                    )}

                                </div>
                            ) : (

                                <div className="prose dark:prose-invert">
                                    <MarkdownPreview source={content} className="prose dark:prose-invert" />
                                </div>
                                
                            )
                            } */}
              <div className="prose dark:prose-invert">
                <MarkdownPreview
                  source={content}
                  className="prose dark:prose-invert"
                />
              </div>
            </div>
            <ThreadDetailActionMenu threadId={id} />
          </div>
        </div>
      </div>

      {posts &&
        posts.items.map((post, i) => (
          <Post key={i} {...post} threadAuthorId={author?.id} />
        ))}

      {!is_closed && <ThreadDetailCreatePost {...thread} />}
      <Pagination total={posts.total} />
    </div>
  );
}
