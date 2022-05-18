package com.smartparking.service.impl;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.smartparking.dto.DistrictDTO;
import com.smartparking.entity.DistrictEntity;
import com.smartparking.mapper.DistrictMapper;
import com.smartparking.repository.DistrictRepository;
import com.smartparking.repository.ProvinceRepository;
import com.smartparking.service.IDistrictService;


@Service
public class DistrictService implements IDistrictService{

	@Autowired
	private DistrictRepository repository;
	
	@Autowired
	private DistrictMapper mapper;
	
	
	
	
	
	@Autowired ProvinceRepository pro_repo;
	
	@Override
	public List<DistrictDTO> findByIdProvince(String id) {
	
		List<DistrictDTO> list = new ArrayList<DistrictDTO>();
		
			List<DistrictEntity> districts = repository.findByIdProvince(id);
			System.out.println(districts.size());
			for (DistrictEntity item:districts) {
				list.add(mapper.toDTO(item));
			}
			return list;
		
		
		
	}

	@Override
	public DistrictDTO findById(String id) {
		Optional<DistrictEntity> entity = repository.findById(id);
		if (entity.isPresent()) {
			DistrictDTO district = mapper.toDTO(entity.get());
			return district;
		}
		return null;
	}

}
