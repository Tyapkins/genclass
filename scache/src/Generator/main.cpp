#include <cstdio>
#include <string>
#include "generator.h"
#include "config.h"
#include "table.h"
#include <csignal>

const char* usageStr =
	"usage:\n"
	"  gen - interactive mode\n"
	"  gen [attrib table] [batch file] - batch mode\n"
	"  gen [config] [attrib table] [rq count] [output file] - silent mode\n"
	"  gen help - print this help\n";

const char* help =
	"Available commands:\n"
	"  table FILE - load table named FILE\n"
	"  rate TIME - set discretion rate (in seconds)\n"
	"  generate CONFIG REQ_COUNT OUTPUT_FILE - generate REQ_COUNT requests\n"
	"    using CONFIG file and write them into OUTPUT_FILE\n"
	"  debug on|off - set generator debugging (default: off)\n"
	"  info - get current settings\n"
	"  clear - clear the screen\n"
	"  exit - finish the program\n"
	"  help - print this help\n";

const char* wrongStr =
	"Wrong command! Please try again";

const char* greeting = "> ";

//constexpr int MAX_STR = 256;

CGenerator* CurrentGenerator = nullptr;

void usage()
{
	printf("%s", usageStr);
}

void wrong()
{
	printf("%s\n", wrongStr);
}

void print(const char* s)
{
	printf("%s", s);
	fflush(stdout);
}

void ok()
{
	printf(" OK\n");
}

void greet()
{
	printf("%s", greeting);
	fflush(stdout);
}

void interrupt(int)
{
	if(CurrentGenerator){
		CurrentGenerator->Reset();
		CurrentGenerator = nullptr;
	}else{
		printf("\nPlease type 'exit' to quit the program\n");
		greet();
	}
}

int interactive(int n, char* name_in, char* name_out)
{
    std::string name_ins = std::string(name_in);
    std::string name_outs = std::string(name_out);
    auto* tablePtr = new CObjectTable("../table.json");
    CConfigReader configReader;
    for (int i = 0; i <= n; i++)
    {
    	//printf("Iteration number %s\n with %d\n", (name_ins + std::to_string(i) + std::string(".ini")).c_str(), i);
        TGeneratorConfig config = configReader.ReadFromFile((name_ins + std::to_string(i) + std::string(".ini")).c_str());
        //printf("End of iteration 00!");
        CGenerator generator(config, *tablePtr);
        //printf("End of iteration 1!");
        CurrentGenerator = &generator;
        generator.SetDebugEnabled(false);
        //printf("End of iteration 2!");
        generator.SetDiscretRate(900);
        generator.Generate((name_outs + std::to_string(i) + std::string(".txt")).c_str(), 1000000);
        CurrentGenerator = nullptr;
        //printf("End of iteration 3!");
    }
    return 0;
    /*printf("%s", help);
    char buf[256];
    char tableName[256];
    time_t discretRate = 900;
    bool debugEnabled = false;
    CObjectTable* tablePtr = 0;
	while(greet(), scanf("%255s", buf) > 0){
	try{
		std::string bufStr(buf);
		if(bufStr == "exit"){
			return 0;
		}else if(bufStr == "help"){
			printf("%s", help);
		}else if(bufStr == "table"){
			scanf("%255s", tableName);
			if(tablePtr != nullptr){
				delete tablePtr;
				//tablePtr = 0;
			}
			print("Opening table...");
			tablePtr = new CObjectTable(tableName);
			ok();
			printf("Table is set to %s\n", tableName);
		}else if(bufStr == "rate"){
			scanf("%lu", &discretRate);
			printf("Set discretion rate to %lu seconds\n", discretRate);
		}else if(bufStr == "generate"){
			if(tablePtr == nullptr){
				printf("Please open the table first\n");
				continue;
			}
			char outputFile[256];
			char configFile[256];
			size_t count;
			scanf("%255s %lu %255s", configFile, &count, outputFile);

			CConfigReader configReader;
			TGeneratorConfig config = configReader.ReadFromFile(configFile);
			CGenerator generator(config, *tablePtr);
			CurrentGenerator = &generator;
			generator.SetDebugEnabled(debugEnabled);
			generator.SetDiscretRate(discretRate);
			generator.Generate(outputFile, count);
			CurrentGenerator = nullptr;
		}else if(bufStr == "debug"){
			scanf("%255s", buf);
			std::string mode = buf;
			if(mode == "enable" || mode == "on"){
				debugEnabled = true;
				printf("Debugging enabled\n");
			}else if(mode == "disable" || mode == "off"){
				debugEnabled = false;
				printf("Debugging disabled\n");
			}else{
				wrong();
			}
		}else if(bufStr == "info"){
			printf("Discretion rate: ");
			if(discretRate > 0){
				printf("%lu seconds\n", discretRate);
			}else{
				printf("not set\n");
			}
			printf("Table: %s\n", tablePtr ? tableName : "not set");
			printf("Debug: %s\n", debugEnabled ? "enabled" : "disabled");
		}else if(bufStr == "clear"){
			system("clear");
			system("clear");
		}else{
			wrong();
		}
		}catch(const char* s){
			printf("%s\n", s);
		}
	}
	return 1;*/
}

/*
Syntax:
configFile discretRate count outputFile
*/
int batch(char** argv)
{
	const char* tableFile = argv[1];
	const char* batchFile = argv[2];
	FILE* batch = fopen(batchFile, "r");
	if(!batch){
		printf("Error: cannot open batch file %s\n", batchFile);
		return 1;
	}
	print("Opening table...");
	CObjectTable table(tableFile);
	ok();
	size_t count, discretRate;
	char configFile[256];
	char outputFile[256];
	while(fscanf(batch, "%255s %lu %lu %255s",
			configFile, &discretRate, &count, outputFile) == 3){
		CConfigReader configReader;
		TGeneratorConfig config = configReader.ReadFromFile(configFile);
		CGenerator generator(config, table);
		generator.SetDiscretRate(discretRate);
		generator.Generate(outputFile, count);
	}
	fclose(batch);
	return 0;
}

int silent(char **argv)
{
	const char* configFileName = argv[1];
	const char* tableFileName = argv[2];
	size_t totalRequestCount = atoi(argv[3]);
	const char* outputFile = argv[4];
	srand(time(nullptr));
	print("Opening config...");
	CConfigReader configReader;
	TGeneratorConfig config = configReader.ReadFromFile(configFileName);
	ok();
	print("Opening table...");
	CObjectTable table(tableFileName);
	ok();
	print("Initializing generator...");
	CGenerator generator(config, table);
	generator.SetDiscretRate(3600); // 1 hour
	ok();
	print("Generating...");
	generator.Generate(outputFile, totalRequestCount);
	ok();
	printf("Finished!\n");
	return 0;
}

void welcome()
{
	//system("clear");
	//system("clear");
	printf("\n\nWelcome to SCache Dataset Generator v0.3!\n\n");
}

int main(int argc, char** argv)
{
	if(argc <= 4){
		signal(SIGINT, interrupt);
		welcome();
		return interactive(atoi(argv[1]), argv[2], argv[3]);
	}
	if(argc == 5 && argv[4] == std::string("help")){
		usage();
		return 0;
	}
	if(argc == 5 && argv[4] == std::string("nosignal")){
		welcome();
		return interactive(atoi(argv[1]), argv[2], argv[3]);
	}
	if(argc == 5){
		welcome();
		return batch(argv);
	}
	if(argc == 6){
		welcome();
		return silent(argv);
	}
	usage();
	return 1;
}
