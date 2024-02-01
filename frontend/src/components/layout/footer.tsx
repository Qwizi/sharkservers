import { Github } from "lucide-react";
import Link from "next/link";

const Footer = () => {
  return (
    <footer className="border-t-2 border-slate-800 p-12">
      <div className="container grid pt-2 grid-cols-1 md:grid-cols-3 text-center">
        <div>
          <span className="text-slate-200">
            <Link
              href="https://github.com/Qwizi/sharkservers-web"
              target="_blank"
            >
              <Github />
            </Link>
          </span>
        </div>
        <div>
          <span className="text-slate-200">© 2023 SharkServers.pl</span>
        </div>
        <div>
          <span className="text-slate-200">
            Strona stworzona przez{" "}
            <Link href="https://github.com/Qwizi">Qwizi</Link>
          </span>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
