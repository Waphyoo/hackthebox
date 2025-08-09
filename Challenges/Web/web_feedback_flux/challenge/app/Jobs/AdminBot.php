<?php

namespace App\Jobs;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use HeadlessChromium\BrowserFactory;
use Illuminate\Support\Facades\Log;

class AdminBot implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    /**
     * Create a new job instance.
     */
    public function __construct()
    {
        //
    }
    
    /**
     * Execute the job.
     */
    public function handle(): void
    {
        $flagPath = '/flag.txt';
        if (!file_exists($flagPath) || !is_readable($flagPath)) {
            Log::error("Flag file not found or unreadable at $flagPath");
            return;
        }

        $flag = trim(file_get_contents($flagPath));
        $browserFactory = new BrowserFactory();
        $domain = '127.0.0.1';

        $browser = $browserFactory->createBrowser([
            "noSandbox" => true,
        ]);

        try {
            $page = $browser->createPage();

            $page->navigate('http://127.0.0.1:8000')->waitForNavigation();

            $page->evaluate(sprintf(
                'localStorage.setItem("flag", "%s"); console.log("Flag stored in localStorage");',
                $flag
            ));
            $page->evaluate('console.log("Flag in localStorage:", localStorage.getItem("flag"));');
            $page->navigate('http://127.0.0.1:8000/feedback')->waitForNavigation();

            usleep(2000000);

        } catch (\Exception $e) {
            Log::error("Error in AdminBot job: " . $e->getMessage());
        } finally {
            $browser->close();
        }
    }
}