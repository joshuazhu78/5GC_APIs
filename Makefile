AsSessionWithQoS: TS29122_AsSessionWithQoS.yaml
	openapi-generator-cli generate \
			-i $< \
			-g go \
				--package-name=models \
			-o $@ \

clean:
	rm -rf AsSessionWithQoS