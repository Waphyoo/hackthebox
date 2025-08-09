<?php

namespace App\Http\Controllers;

use App\Models\Feedback;
use Illuminate\Http\Request;
use App\Jobs\AdminBot;
use TYPO3\HtmlSanitizer\Behavior;
use TYPO3\HtmlSanitizer\Behavior\NodeInterface;
use TYPO3\HtmlSanitizer\Sanitizer;
use TYPO3\HtmlSanitizer\Visitor\CommonVisitor;


class FeedbackController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        $feedback = Feedback::query()->orderBy('id', 'desc')->paginate(20);
        return view('index', ['feedbacks' => $feedback]);
    }

    /**
     * Show the form for creating a new resource.
     */
    public function create()
    {
        return view('create');
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        $data = $request->validate([
            'feedback' => ['required', 'string']
        ]);

        $commonAttrs = [
            new Behavior\Attr('id'),
            new Behavior\Attr('class'),
            new Behavior\Attr('data-', Behavior\Attr::NAME_PREFIX),
        ];
        $hrefAttr = (new Behavior\Attr('href'))
            ->addValues(new Behavior\RegExpAttrValue('#^https?://#'));
        
        $behavior = (new Behavior())
            ->withFlags(Behavior::ENCODE_INVALID_TAG | Behavior::ENCODE_INVALID_COMMENT)
            ->withoutNodes(new Behavior\Comment())
            ->withNodes(new Behavior\CdataSection())
            ->withTags(
                (new Behavior\Tag('div', Behavior\Tag::ALLOW_CHILDREN))
                    ->addAttrs(...$commonAttrs),
                (new Behavior\Tag('a', Behavior\Tag::ALLOW_CHILDREN))
                    ->addAttrs(...$commonAttrs)
                    ->addAttrs($hrefAttr->withFlags(Behavior\Attr::MANDATORY)),
                (new Behavior\Tag('br'))
            )
            ->withNodes(
                (new Behavior\NodeHandler(
                    new Behavior\Tag('typo3'),
                    new Behavior\Handler\ClosureHandler(
                        static function (NodeInterface $node, ?DOMNode $domNode): ?DOMNode {
                            return $domNode === null
                                ? null
                                : new DOMText(sprintf('%s says: "%s"',
                                    strtoupper($domNode->nodeName),
                                    $domNode->textContent
                                ));
                        }
                    )
                ))
            );
        
        $visitors = [new CommonVisitor($behavior)];
        $sanitizer = new Sanitizer($behavior, ...$visitors);
        $data['feedback'] = $sanitizer->sanitize($data['feedback']);

        Feedback::create($data);

        AdminBot::dispatch();
        return to_route('feedback.create')->with('message', 'Feedback submitted!');
    }

}
