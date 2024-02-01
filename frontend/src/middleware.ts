import { withAuth } from "next-auth/middleware";
import { redirect } from "next/navigation";

export default withAuth(function middleware(req) {}, {
  callbacks: {
    authorized: ({ req, token }) => {
      if (
        req.nextUrl.pathname.startsWith("/forum/create") ||
        req.nextUrl.pathname.startsWith("/settings") ||
        req.nextUrl.pathname.startsWith("/admin")
      ) {
        if (req.nextUrl.pathname.startsWith("/admin")) {
          if (!token?.is_superuser) {
            return false;
          }
        }
        return !!token;
      }
      return true;
    },
  },
});
