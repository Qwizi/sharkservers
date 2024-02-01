import {ApiClient} from "./src/client";

export *  from "./src/client"

const SharkServersClient = new ApiClient({
    BASE: "http://localhost",
});

export {SharkServersClient}

