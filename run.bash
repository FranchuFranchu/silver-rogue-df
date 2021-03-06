command -v python3 -c "" >/dev/null 2>&1 || {
 echo >&2 "Python3 must be installed and added to PATH";
 exit 1;
}
all_modules_installed=1
installed_mods=` pip3 freeze | sed --expression='s/\(.*\)==\(.*\)/\1/' | tr $'\n' $' '`

while read -r line 
do
	# echo "Checking if $line is installed" # uncomment this if you want logs
	case "$line" in *installed_mods* )
		echo "$line is not pip-installed!"
		all_modules_installed=0
		break
		;;
	esac
done < "./requirements.txt"
if [ $all_modules_installed -eq 1 ]  
then
	cd rogue
	python3 main.py ${@}
fi

