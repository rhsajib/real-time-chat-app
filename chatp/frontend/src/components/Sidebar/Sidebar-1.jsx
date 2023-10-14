import React from "react";

const Sidebar = () => {
    return (
        <div>
            <aside class="bg-gray-800 text-white w-1/5 h-screen fixed left-0 top-0 overflow-y-auto">
                <div class="p-4 text-center">
                    <h1 class="text-2xl font-semibold">My App</h1>
                </div>

                <nav class="px-4">
                    <ul class="space-y-2">
                        <li>
                            <a href="#" class="block py-2">
                                Home
                            </a>
                        </li>
                        <li>
                            <a href="#" class="block py-2">
                                About
                            </a>
                        </li>
                        <li>
                            <a href="#" class="block py-2">
                                Services
                            </a>
                        </li>
                        <li>
                            <a href="#" class="block py-2">
                                Contact
                            </a>
                        </li>
                    </ul>
                </nav>
            </aside>
        </div>
    );
};

export default Sidebar;
