Feature: run the cli,
  call the docs command,
  exit the cli

  Scenario: run the cli
     Given we have iawscli installed
      when we run iawscli
      then we see iawscli prompt

  Scenario: run the cli and exit
     Given we have iawscli installed
      when we run iawscli
      and we wait for prompt
      and we send "ctrl + d"
      then iawscli exits
