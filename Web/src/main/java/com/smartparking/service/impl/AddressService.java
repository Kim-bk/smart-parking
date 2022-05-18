package com.smartparking.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.smartparking.dto.AddressDTO;
import com.smartparking.entity.AddressEntity;
import com.smartparking.mapper.AddressMapper;
import com.smartparking.repository.AddressRepository;
import com.smartparking.service.IAddressService;


@Service
public class AddressService implements IAddressService{

	@Autowired
	private AddressRepository repository;
	
	@Autowired
	private AddressMapper mapper;

	@Override
	public AddressDTO save(AddressDTO address) {
		AddressEntity addressEntity = mapper.toEntity(address);
		AddressEntity addSave = repository.save(addressEntity);
		return mapper.toDTO(addSave);
	}
	
	
}
