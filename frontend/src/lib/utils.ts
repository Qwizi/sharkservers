import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"
 
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const dateTimeFormatter = new Intl.DateTimeFormat("pl-PL", {dateStyle: "medium", timeStyle: "short"})
export const dateFormatter = new Intl.DateTimeFormat("pl-PL", {dateStyle: "short"})

export function hasScope(roles: any, scope: string) {
  let has = false
  roles.map((role) => {
    role.scopes.map((item) => {
      const scopeSplit = scope.split(":")
      const app_name = scopeSplit[0]
      const value = scopeSplit[1] 
      if (item.app_name == app_name && item.value == value) {
        has = true
      }
    })
  })
  
  return has
}

import { getCsrfToken } from 'next-auth/react';
import { init } from '../../node_modules/next-auth/core/init'; // You have to import it like this
import getAuthorizationUrl from '../../node_modules/next-auth/core/lib/oauth/authorization-url';
import { setCookie } from '../../node_modules/next-auth/next/utils';
import type { NextAuthOptions } from 'next-auth';
import { getServerSession } from 'next-auth';
import { GetServerSidePropsContext } from 'next';
import { IncomingMessage } from 'http';
import { NextApiRequestCookies } from 'next/dist/server/api-utils';

async function getServerSignInUrl(
  req: IncomingMessage,
  cookies: NextApiRequestCookies,
  authOptions: NextAuthOptions
) {
  const { options, cookies: initCookies } = await init({
    action: 'signin',
    authOptions,
    isPost: true,
    cookies,
    csrfToken: await getCsrfToken({ req }),
    callbackUrl: req.url,
  });
  const { redirect, cookies: authCookies } = await getAuthorizationUrl({options, query: {} });
  return {
    redirect,
    cookies: [...initCookies, ...authCookies],
  };
}