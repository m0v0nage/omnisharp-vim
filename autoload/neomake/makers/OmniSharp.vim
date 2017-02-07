if !(has('python') || has('python3'))
  finish
endif

let s:pycmd = has('python3') ? 'python3' : 'python'

let s:save_cpo = &cpo
set cpo&vim

function! neomake#makers#OmniSharp#get(target)
  let closure = {
              \ 'target': a:target,
              \ 'script': fnameescape(g:omnisharp_python_path '/codecheck.py')}

  function! closure.fn()
    let l:args = [
                \ self.script,
                \ self.target,
                \ get(b:, 'OmniSharp_host', g:OmniSharp_host),
                \ '%:p']
    return l:args
  endfunction

  return {
        \ 'exe': s:pycmd
        \ 'args': closure,
        \ 'errorformat': '%f \(%l %c\): %terror %m,' .
              \'%f \(%l %c\): %tarning %m'
        \ }
endfunction

function! neomake#makers#OmniSharp#issues()
  return neomake#makers#OmniSharp#get('--code-issues')
endfunction
function! neomake#makers#OmniSharp#code_checker()
  return neomake#makers#OmniSharp#get('--code-check')
endfunction
function! neomake#makers#OmniSharp#semantic()
  return neomake#makers#OmniSharp#get('--semantic-errors')
endfunction
function! neomake#makers#OmniSharp#syntax()
  return neomake#makers#OmniSharp#get('--syntax-errors')
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo

" vim:nofen:fdl=0:ts=2:sw=2:sts=2
